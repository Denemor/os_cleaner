from cosmic_chartreux.app import create_app


application = create_app()


if __name__ == "__main__":
    application.run(port=5001)