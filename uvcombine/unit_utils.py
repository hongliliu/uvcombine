from astropy import units as u
from astropy import wcs
import radio_beam

from .uvcombine import file_in

def convert_to_casa(hdu):
    """
    Convert a FITS HDU to casa-compatible units, i.e., Jy/beam
    """
    hdu = file_in(hdu)[0]

    beam = radio_beam.Beam.from_fits_header(hdu.header)

    if hdu.header['BUNIT'] == 'K':
        imwcs = wcs.WCS(hdu.header)
        cfreq = imwcs.sub([wcs.WCSSUB_SPECTRAL]).wcs_world2pix([0], 0)[0][0]
        hdu.data = u.Quantity(hdu.data,
                              unit=u.K).to(u.Jy,
                                           u.brightness_temperature(beam,
                                                                    cfreq*u.Hz)).value
    elif u.Unit(hdu.header['BUNIT']).is_equivalent(u.MJy/u.sr):
        hdu.data = u.Quantity(hdu.data,
                              u.Unit(hdu.header['BUNIT'])).to(u.Jy/beam).value

    return hdu
