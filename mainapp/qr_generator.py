# Import QR Code library
import qrcode


def qr_generator(data):
    # Create qr code instance
    qr = qrcode.QRCode(
        version = 1,
        error_correction = qrcode.constants.ERROR_CORRECT_H,
        box_size = 10,
        border = 4,
    )

    # Add data
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image()
    img.save("qr_codes/image.png")


if __name__ == '__main__':
    qr_generator({"borrow_id":1})