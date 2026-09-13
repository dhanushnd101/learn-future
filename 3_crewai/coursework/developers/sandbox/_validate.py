import app
from app import create_demo

def validate():
    demo = create_demo()
    assert demo is not None
    print("Gradio demo successfully created and validated!")

if __name__ == "__main__":
    validate()
