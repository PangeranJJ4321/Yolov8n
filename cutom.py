import cv2
import numpy as np

def generate_checkerboard(square_size_mm=25, pattern_size=(9,6), filename='checkerboard_25mm.png'):
    squares_x = pattern_size[0] + 1
    squares_y = pattern_size[1] + 1

    square_size_px = 200  # arbitrary — nanti kamu print disesuaikan skalanya
    img_size = (squares_x * square_size_px, squares_y * square_size_px)

    board = np.zeros((img_size[1], img_size[0]), np.uint8)
    for y in range(squares_y):
        for x in range(squares_x):
            if (x + y) % 2 == 0:
                cv2.rectangle(board, (x*square_size_px, y*square_size_px),
                              ((x+1)*square_size_px, (y+1)*square_size_px), 255, -1)
    cv2.imwrite(filename, board)
    print(f"✅ Checkerboard tersimpan: {filename}")

generate_checkerboard()
