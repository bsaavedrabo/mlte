## Distribution Docker Setup

This readme briefly explains how to use this set of dockerfiles for a Docker-based deployment. It will be later integrated into the main documentation.

 - This set of Docker files are not intended to be packaged inside a MLTE distributable, but to be manually deployed on a server for deployment.
 - These Docker files assume a MLTE package is created, either locally or published yo PyPi, and build images based on this.

 The steps to do a deployment based on these files are:

 1. Select a MLTE wheel to use.
    - If using a MLTE package already published to PyPi, modify ``Dockerfile.wheel`` commenting lines 11 and 12 and uncommenting line 13. This will pull the package from PyPi when building the image.
    - If creating a wheel from source code, go to the main repo folder and run ``bash build.sh``
 1. Create proper .env configuration files for all components in the system:
    1. Create a ``.env`` file with a ``FRONTEND_PORT`` (defaults to ``8000``) and ``BACKEND_PORT`` (defaults to ``8080``) values, that have to match the configs for both components.
    1. Create a ``.env.posgres`` file with values for ``POSTGRES_USER``, ``POSTGRES_PASSWORD``, and ``POSTRGRES_DB``, as defined in the official PostgreSQL Docker Hub image.
    1. Create a ``.env.backend`` file based on the one at ``mlte/cli/.env.backend`` file with the proper config for the deployed Backend:
       -  Usually ``APP_HOST`` will need to be ``0.0.0.0``, and ``APP_PORT`` has to match the one in ``.env``
       - ``ALLOWED_ORIGINS`` will likely need to be ``["*"]`` to allow broad access from any web browser.
       - ``JWT_SECRET_KEY`` should be configured to a deployment-specific secret.
       - ``BACKEND_URI`` should have the ``postgresql://`` prefix, and the rest should match the user, password and DB name in the ``.env.postgres`` file.
    1. Create a ``.env.frontend`` file based on the one at ``mlte/cli/.env.frontend`` file with the proper config for the deployed Frontend (usually ``APP_HOST`` will need to be ``0.0.0.0``, and ``APP_PORT`` has to match the one in ``.env``).
1. Copy all files in this folder, including the new ``.env`` configurations and the created wheel (if applicable), to the server to be deployed.
1. Run ``bash start.sh`` to run the system. You can "CTRL+C" and it will continue running in the background.
    - To stop it if needed, run ``bash stop.sh``
