class Config:
    VALID_MODEL_TYPES = {"OFFICIAL", "CUSTOM"}
    model = "yolov5nu.pt"
    model_type = "OFFICIAL"  # OFFICIAL for Ultralytics, CUSTOM for PyTorch

    @classmethod
    def validate(cls):
        cls.model_type = cls.model_type.upper()
        if cls.model_type not in cls.VALID_MODEL_TYPES:
            raise ValueError(f"Invalid model_type: {cls.model_type}. Must be one of {cls.VALID_MODEL_TYPES}")
        if not cls.model.endswith(".pt"):
            raise ValueError(f"Model file {cls.model} must be a .pt file")

def main():
    Config.validate()
    print(f"Config: model={Config.model}, type={Config.model_type}")

if __name__ == "__main__":
    main()
