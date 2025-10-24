from ultralytics import YOLO
import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Train/validate/predict YOLOv8 on Roboflow potholes dataset"
    )
    parser.add_argument(
        "--mode",
        choices=["train", "val", "predict"],
        default="train",
        help="Execution mode",
    )
    parser.add_argument(
        "--data",
        default="G:/Yolov8n/datasets/potholes_raw/data.yaml",
        help="Path to data.yaml",
    )
    parser.add_argument(
        "--model",
        default="yolov8n.pt",
        help="Model path or alias (e.g., yolov8n.pt or runs/.../best.pt)",
    )
    parser.add_argument("--imgsz", type=int, default=640, help="Image size")
    parser.add_argument("--batch", type=int, default=8, help="Batch size")
    parser.add_argument("--epochs", type=int, default=50, help="Training epochs")
    parser.add_argument(
        "--name",
        default="yolov8n-potholes",
        help="Run name for outputs under runs/",
    )
    parser.add_argument(
        "--split",
        choices=["val", "test"],
        default="val",
        help="Validation split to use when mode=val",
    )
    parser.add_argument(
        "--source",
        default="G:/Yolov8n/datasets/potholes_raw/valid/images",
        help="Source path for prediction when mode=predict (file/dir/webcam)",
    )
    parser.add_argument(
        "--conf",
        type=float,
        default=0.25,
        help="Confidence threshold for prediction",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    model = YOLO(args.model)

    if args.mode == "train":
        model.train(
            data=args.data,
            epochs=args.epochs,
            imgsz=args.imgsz,
            batch=args.batch,
            name=args.name,
        )
        return

    if args.mode == "val":
        # Prefer explicit split if supported by current ultralytics version
        try:
            model.val(data=args.data, imgsz=args.imgsz, batch=args.batch, split=args.split)
        except TypeError:
            # Fallback if split argument isn't available; validates on default split
            model.val(data=args.data, imgsz=args.imgsz, batch=args.batch)
        return

    if args.mode == "predict":
        model.predict(
            source=args.source,
            imgsz=args.imgsz,
            conf=args.conf,
            name=f"{args.name}-predict",
            save=True,
        )
        return


if __name__ == "__main__":
    main()
