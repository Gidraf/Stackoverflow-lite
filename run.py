"""run app"""
from app import create_app

APP=create_app('development')

if __name__=="__main__":
    """rujn the file"""
    APP.run()
