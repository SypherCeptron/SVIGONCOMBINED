
import numpy as np


def detect_blur_fft(image, radius=60, thresh=10):
    # To get Hieght and Width
    (h, w) = image.shape
    # To get the center coordinates
    (cX, cY) = (int(w / 2.0), int(h / 2.0))

    # compute the FFT to find the frequency transform, then shift
    fft = np.fft.fft2(image)
    fftShift = np.fft.fftshift(fft)

    # zero-out the center of the FFT shift
    fftShift[cY - radius:cY + radius, cX - radius:cX + radius] = 0
    # apply inver fftshift
    fftShift = np.fft.ifftshift(fftShift)
    # apply inverse fft
    recon = np.fft.ifft2(fftShift)

    # compute the magnitude spectrum of the reconstructed image,
    magnitude = 20 * np.log(np.abs(recon))
    # then compute the mean of the magnitude values
    mean = np.mean(magnitude)

    return (mean, mean <= thresh)
