"""AiiDA parsers for output of network executable."""
# pylint: disable=useless-super-delegation
import re
import math


class KeywordParser():
    """Generic keyword-value parser class.

    Reused by more specific parsers.
    """

    keywords = {
        'keyword1': [float, 'unit1'],
        'keyword2': [int, 'unit2'],
    }

    @classmethod
    def parse(cls, string):
        """ Parse zeo++ keyword format

        Example string:

        keyword1: 12234.32312  keyword2: 1

        parameters
        ----------
        string: string
          string with keywords

        return
        ------
        results: dict
          dictionary of output values
        """
        results = {}

        regex = r'{}:\s?([\d\.]*)'
        for keyword, val in cls.keywords.items():
            ktype, kunit = val
            regex_rep = regex.format(re.escape(keyword))
            match = re.search(regex_rep, string)
            if match is None:
                raise ValueError('Keyword {} not specified'.format(keyword))

            value = match.group(1)
            if value == '':
                value = 0
                # uncomment this when #1 is fixed
                #raise ValueError(
                #    "No value specified for keyword {}".format(keyword))

            results[keyword] = ktype(value)
            results[keyword + '_unit'] = kunit

        return results


class PoreVolumeParser(KeywordParser):
    """Parse PoreVolume output of network executable."""

    keywords = {
        'Unitcell_volume': [float, 'A^3'],
        'Density': [float, 'g/cm^3'],
        'POAV_A^3': [float, 'A^3'],
        'POAV_Volume_fraction': [float, None],
        'POAV_cm^3/g': [float, 'cm^3/g'],
        'PONAV_A^3': [float, 'A^3'],
        'PONAV_Volume_fraction': [float, None],
        'PONAV_cm^3/g': [float, 'cm^3/g'],
    }

    @classmethod
    def parse(cls, string):
        """ Parse zeo++ .volpo format

        Example volpo string:

        @ EDI.volpo Unitcell_volume: 307.484   Density: 1.62239
        POAV_A^3: 131.284 POAV_Volume_fraction: 0.42696 POAV_cm^3/g: 0.263168
        PONAV_A^3: 0 PONAV_Volume_fraction: 0 PONAV_cm^3/g: 0

        parameters
        ----------
        string: string
          string in volpo format

        return
        ------
        results: dict
          dictionary of output values
        """
        return super(PoreVolumeParser, cls).parse(string)


class AVolumeParser(KeywordParser):
    """Parse AVolume output of network executable."""

    keywords = {
        'Unitcell_volume': [float, 'A^3'],
        'Density': [float, 'g/cm^3'],
        'AV_A^3': [float, 'A^3'],
        'AV_Volume_fraction': [float, None],
        'AV_cm^3/g': [float, 'cm^3/g'],
        'NAV_A^3': [float, 'A^3'],
        'NAV_Volume_fraction': [float, None],
        'NAV_cm^3/g': [float, 'cm^3/g'],
    }

    @classmethod
    def parse(cls, string):
        """ Parse zeo++ .vol format

        Example vol string:

        @ EDI.vol Unitcell_volume: 307.484   Density: 1.62239
        AV_A^3: 22.6493 AV_Volume_fraction: 0.07366 AV_cm^3/g: 0.0454022
        NAV_A^3: 0 NAV_Volume_fraction: 0 NAV_cm^3/g: 0

        parameters
        ----------
        string: string
          string in volpo format

        return
        ------
        results: dict
          dictionary of output values
        """
        return super(AVolumeParser, cls).parse(string)


class SurfaceAreaParser(KeywordParser):
    """Parse surface area output of network executable."""

    keywords = {
        'Unitcell_volume': [float, 'A^3'],
        'Density': [float, 'g/cm^3'],
        'ASA_A^2': [float, 'A^2'],
        'ASA_m^2/cm^3': [float, 'm^2/cm^3'],
        'ASA_m^2/g': [float, 'm^2/g'],
        'NASA_A^2': [float, 'A^2'],
        'NASA_m^2/cm^3': [float, 'm^2/cm^3'],
        'NASA_m^2/g': [float, 'm^2/g'],
        'Number_of_channels': [int, None],
        'Channel_surface_area_A^2': [float, 'A^2'],
        'Number_of_pockets': [int, None],
        'Pocket_surface_area_A^2': [float, 'A^2'],
    }

    @classmethod
    def parse(cls, string):
        """ Parse zeo++ .sa format

        Example sa string:

        @ HKUST-1.sa Unitcell_volume: 18280.8   Density: 0.879097   ASA_A^2:
        3545.59 ASA_m^2/cm^3: 1939.51 ASA_m^2/g: 2206.26 NASA_A^2: 0
        NASA_m^2/cm^3: 0 NASA_m^2/g: 0 Number_of_channels: 1
        Channel_surface_area_A^2: 3545.59 Number_of_pockets: 0
        Pocket_surface_area_A^2:

        parameters
        ----------
        string: string
          string in sa format

        return
        ------
        results: dict
          dictionary of output values
        """
        return super(SurfaceAreaParser, cls).parse(string)


class ResParser(KeywordParser):
    """Parse .res output of network executable."""

    keywords = (
        'Largest_included_sphere',
        'Largest_free_sphere',
        'Largest_included_free_sphere',
    )

    @classmethod
    def parse(cls, string):
        """ Parse zeo++ .res format

        Example res string:

        HKUST-1.res    13.19937 6.74621  13.19937

        Containing the diameters of
         * the largest included sphere
         * the largest free sphere
         * the largest included sphere along free sphere path

        parameters
        ----------
        string: string
          string in res format

        return
        ------
        res: dict
          dictionary of output values
        """
        res = {}

        values = string.split()

        if len(values) != 4:
            raise ValueError('Found more than 4 fields in .res format')

        for i in (0, 1, 2):
            keyword = cls.keywords[i]
            res[keyword] = float(values[i + 1])
            res[keyword + '_unit'] = 'A'

        return res


class PoresSizeDistParser():  # pylint: disable=too-few-public-methods
    """Parse pore size distribution output of network executable."""
    @classmethod
    def parse(cls, string):  # pylint: disable=too-many-locals
        """
        Parse zeo++ .psd format, using routines similar to other parsers to avoid additional pandas dependency

        Parameters
        ----------
        string: str
            string in psd format

        Returns
        -------
        results: dict
            dictionary of output values
        """
        def clean_values(float_list):
            """Removes NaN and Inf from list of floats.

            Those are not JSON-serializable:
            https://www.postgresql.org/docs/current/datatype-json.html#JSON-TYPE-MAPPING-TABLE
            """
            return [
                0 if math.isnan(f) or math.isinf(f) else f for f in float_list
            ]

        lines = string.splitlines()
        # remove empty lines
        lines = [l for l in lines if l.strip()]

        # find line where histogram data begins
        header_line = 'Bin Count'
        i = 0
        for i, line in enumerate(lines):
            if header_line in line:
                break
        else:
            raise ValueError('Did not find header line in data')
        # extract histogram data
        bins, counts, cumulatives, derivatives = [], [], [], []
        for line in lines[i + 1:]:
            bin, count, cumulative, derivative = line.split()  # pylint: disable=redefined-builtin
            bins.append(float(bin))
            counts.append(int(count))
            cumulatives.append(float(cumulative))
            derivatives.append(float(derivative))

        psd_dict = {
            'psd': {
                'bins': bins,
                'counts': counts,
                # these can be nan /-nan when the counts are zero
                'cumulatives': clean_values(cumulatives),
                'derivatives': clean_values(derivatives)
            }
        }

        return psd_dict


class ChannelParser():
    """Parse pore channel output of network executable."""
    @classmethod
    def parse(cls, string):  # pylint: disable=too-many-locals
        """ Parse zeo++ .chan format

        Example chan string::

            P8bal_P1.chan   2 channels identified of dimensionality 3 3
            Channel  0  9.92223  3.85084  9.92223
            Channel  1  9.92222  3.85084  9.92222
            P8bal_P1.chan summary(Max_of_columns_above)   9.92223 3.85084  9.92223  probe_rad: 1.8  probe_diam: 3.6


        parameters
        ----------
        string: string
          string in chan format

        return
        ------
        results: list
          dictionary of output values
        """
        lines = string.splitlines()
        # remove empty lines
        lines = [l for l in lines if l.strip()]
        nlines = len(lines)

        # parse header line
        match = re.search(
            r'(\d+) channels identified of dimensionality([\d\s]*)', lines[0])
        if not match:
            raise ValueError(
                'The following string was not recognized as a valid header of the .chan format:\n'
                + lines[0])

        nchannels = int(match.group(1))

        if nchannels == 0:
            dimensionalities = []
        else:
            dimensionalities = list(map(int, match.group(2).split()))

        if nchannels != len(dimensionalities):
            raise ValueError(
                'Number of channels {} does not match number of dimensionalities {}'
                .format(nchannels, len(dimensionalities)))

        if nchannels != nlines - 2:
            raise ValueError(
                'Number of lines in file {} does not equal number of channels {}+2'
                .format(nlines, nchannels))

        # parse remaining lines (last line is discarded)
        dis, dfs, difs = [], [], []
        for i in range(1, nchannels + 1):
            _c, _i, di, df, dif = lines[i].split()  # pylint: disable=invalid-name
            dis.append(float(di))
            dfs.append(float(df))
            difs.append(float(dif))

        pm_dict = {
            'Channels': {
                'Largest_included_spheres': dis,
                'Largest_free_spheres': dfs,
                'Largest_included_free_spheres': difs,
                'Dimensionalities': dimensionalities,
            }
        }
        return pm_dict

