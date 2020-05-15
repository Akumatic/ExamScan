#!/usr/bin/python
# SPDX-License-Identifier: MIT
# Copyright (c) 2019 Akumatic

from scan import image, contours, io, eval

if __name__ == "__main__":
    # BGR Colors
    BGR_R = (0, 0, 255)
    BGR_G = (0, 255, 0)
    BGR_B = (255, 0, 0)

    # Parse cli args
    args = io.parse_args()

    # Reads File
    img = io.read_image(path=args.file, url=args.url)

    # image copies for processing
    img_orig = img.copy()
    img_blur = image.blur(img)
    img_thres = image.threshold(img_blur)
    img_edges = image.edge_detection(img_thres.copy())

    # gather contour data and find boxes. draws boxes
    cnts = contours.find_contours(img_edges)
    cnts_box = contours.find_boxes(cnts)
    img_boxes = image.draw_contours(img_orig.copy(), cnts_box, BGR_G)

    # retrieve the center of all contours and 
    # filters entries too close to each other.
    center_boxes = contours.find_center(cnts_box)
    avg_radius = int(sum([contours.dist_center_topleft(center[2],
        center[:2]) for center in center_boxes]) / len(center_boxes))
    contours.filter_centers(center_boxes, avg_radius)

    # Sort Box data
    #center_boxes = sorted(center_boxes, key=lambda x: (x[1], x[0]))

    # draw center of given contours into original picture
    img_center_boxes = image.draw_circles(img_orig.copy(), center_boxes, BGR_G)

    img_rad = image.draw_circles(img_thres.copy(), center_boxes, BGR_G,
        radius=int(avg_radius))

    center_eval = [(center[0], center[1], image.ratio_black(img_thres, center[:2],
        avg_radius)) for center in center_boxes]

    img_eval = image.eval_image(img_orig.copy(), center_eval, avg_radius)

    evaluation = eval.evaluate(center_eval, args.num, avg_radius)
    print(evaluation)

    if args.comp is not None:
        result = eval.compare(evaluation, io.load_results(args.comp))
        print(result)

    # write result to file if optional flag is given
    if args.iout is not None:
        io.write_image(img_eval, args.iout)
        print(f"Stored image to {args.iout}")

    if args.dout is not None:
        io.store_results(evaluation, args.dout)
        print(f"Stored data to {args.dout}")

    if args.plot:
        io.plot(img_orig, img_blur, img_thres, img_edges,
            img_boxes, img_center_boxes, img_rad, img_eval)