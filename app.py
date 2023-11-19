import streamlit as st
import tensorflow as tf
import matplotlib.pyplot as plt
import os
from io import BytesIO
import zipfile
import base64

# Load the generator and discriminator models
generator =  tf.saved_model.load("Generator")
save_dir = "generated_images"  # Directory to save the generated images

def generate_and_save_images(generator,num_images=1000, save_dir=save_dir):
    noise_dim=50
    # Generate random noise for the specified number of images
    noise = tf.random.normal([num_images, noise_dim])

    # Generate images using the generator
    generated_images = generator(noise, training=False)

    # Create the directory if it does not exist
    os.makedirs(save_dir, exist_ok=True)

    # Calculate the number of rows and columns for the subplot grid
    rows = cols = int(num_images**0.5)
    while rows * cols < num_images:
        cols += 1

    # Save the generated images in a grid
    plt.figure(figsize=(15, 15))
    for i in range(num_images):
        plt.subplot(rows, cols, i + 1)
        plt.imshow(generated_images[i, :, :, 0], cmap='gray')
        plt.axis('off')
        # Save the generated image
        image_path = os.path.join(save_dir, f'generated_image_{i}.png')
        plt.imsave(image_path, generated_images[i, :, :, 0].numpy(), cmap='gray')

    plt.close()


    st.write("Generation Done, Download the images")

    return save_dir, num_images

# Streamlit app
st.title("Image Generator App")
# Allow the user to input the number of images manually
num_images = st.number_input("Enter the number of images to generate", min_value=1, value=10, step=1)

if st.button("Generate Images"):
    st.markdown("Generating Images...")
    # Generate and save the images
    save_dir, num_images = generate_and_save_images(generator, num_images)
    st.success(f"Images generated and saved in {save_dir}")

    # Zip the generated images
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED) as zip_file:
        for i in range(num_images):
            image_path = os.path.join(save_dir, f'generated_image_{i}.png')
            zip_file.write(image_path, f'generated_image_{i}.png')

    # Download the zip file
    st.markdown("### Download Generated Images")
    st.markdown(
        f"Click the link below to download the zip file containing the generated images: [Download Zip File](data:application/zip;base64,{base64.b64encode(zip_buffer.getvalue()).decode()})"
    )
