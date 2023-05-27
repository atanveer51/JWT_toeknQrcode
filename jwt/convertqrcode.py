import qrcode

access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg1MTA1NTY0LCJqdGkiOiJjMDY3NWNlYWUzODI0MDQ0OTFiYzViOWY2NjVjZDA5NSIsInVzZXJfaWQiOjN9.Hk2U9_HELusAi9YZerjaLqFy6lUzIyJxwGiaQiulYSw"

# Create a QR code instance
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4,
)

# Add the access token as data to the QR code
qr.add_data(access_token)
qr.make(fit=True)

# Create an image from the QR code
image = qr.make_image(fill_color="black", back_color="white")

# Save the image to a file
image.save("access_token_qr_code.png")
