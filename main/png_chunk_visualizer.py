from PIL import Image

def count_png_chunks(png_file):
    img = Image.open(png_file)

    chunks = img.info.get('png')

    if chunks:
        print(f"Number of chunks found: {len(chunks)}")
    else:
        print("No PNG chunks found in the image.")

# if __name__ == "__main__":
#     png_file = r'8 oz.png'
#     count_png_chunks(png_file)


def read_png_chunks(file_path):
    chunks = []
    with open(file_path, 'rb') as f:
        # Check the PNG signature
        signature = f.read(8)
        if signature != b'\x89PNG\r\n\x1a\n':
            raise ValueError("Not a valid PNG file")

        while True:
            # Read chunk length (4 bytes, big-endian)
            length_data = f.read(4)
            if len(length_data) == 0:
                break  # End of file reached

            length = int.from_bytes(length_data, 'big')
            # Read chunk type (4 bytes)
            chunk_type = f.read(4).decode('ascii')
            # Read chunk data
            chunk_data = f.read(length)
            
            # Read CRC (4 bytes)
            crc = f.read(4)

            chunks.append((chunk_type, length))
            
            if chunk_type == 'IEND':
                break
            # if chunk_type == 'IDAT':
            #     print(chunk_data)
            #     break
            


    return chunks

if __name__ == "__main__":
    png_file = r'8 oz.png'
    chunks = read_png_chunks(png_file)
    for i, (chunk_type, length) in enumerate(chunks):
        print(f"Chunk {i + 1}: {chunk_type}, Length: {length}")
    
    print(f"Total number of chunks: {len(chunks)}")