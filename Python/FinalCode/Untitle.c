#include <stdio.h>
#include <stdint.h>

#pragma pack(1)

typedef struct {
    uint16_t type;
    uint32_t size;
    uint16_t reserved1;
    uint16_t reserved2;
    uint32_t offset;
} BMPHeader;

typedef struct {
    uint32_t size;
    int32_t width;
    int32_t height;
    uint16_t planes;
    uint16_t bitsPerPixel;
    uint32_t compression;
    uint32_t imageSize;
    int32_t xPixelsPerMeter;
    int32_t yPixelsPerMeter;
    uint32_t colorsUsed;
    uint32_t colorsImportant;
} BMPInfoHeader;

typedef struct {
    BMPHeader header;
    BMPInfoHeader infoHeader;
} BMPFile;

void read_bmp_file(const char* file_path, BMPFile* bmpFile) {
    FILE* file = fopen(file_path, "rb");
    if (file == NULL) {
        printf("Unable to open image file.\n");
        return;
    }

    // Read BMP header
    fread(&(bmpFile->header), sizeof(BMPHeader), 1, file);

    // Check if it's a BMP file
    if (bmpFile->header.type != 0x4D42) {
        printf("Invalid BMP file.\n");
        fclose(file);
        return;
    }

    // Read BMP info header
    fread(&(bmpFile->infoHeader), sizeof(BMPInfoHeader), 1, file);

    // Check if it's a supported BMP format (uncompressed 24-bit)
    if (bmpFile->infoHeader.bitsPerPixel != 24 || bmpFile->infoHeader.compression != 0) {
        printf("Unsupported BMP format.\n");
        fclose(file);
        return;
    }

    fclose(file);
}

int main() {
    const char* file_path = "sample.bmp";
    BMPFile bmpFile;
    read_bmp_file(file_path, &bmpFile);

    // Access header data
    printf("BMP Header:\n");
    printf("Type: 0x%X\n", bmpFile.header.type);
    printf("Size: %u\n", bmpFile.header.size);
    printf("Offset: %u\n", bmpFile.header.offset);

    printf("\nBMP Info Header:\n");
    printf("Size: %u\n", bmpFile.infoHeader.size);
    printf("Width: %d\n", bmpFile.infoHeader.width);
    printf("Height: %d\n", bmpFile.infoHeader.height);
    printf("Bits per Pixel: %u\n", bmpFile.infoHeader.bitsPerPixel);
    printf("Image Size: %u\n", bmpFile.infoHeader.imageSize);

    return 0;
}
