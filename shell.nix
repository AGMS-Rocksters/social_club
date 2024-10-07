{ pkgs ? import <nixpkgs> { } }:
with pkgs.python311Packages;
pkgs.mkShell {
  packages = [
    (pkgs.python311.withPackages (python-pkgs: with python-pkgs; [
      django
      python-dotenv
      # (djangorestframework.override { django = django_5; })
      djangorestframework
      djangorestframework-simplejwt
      gunicorn
      uvicorn
      six
      psycopg2

      ipython
      django-extensions
      coverage
    ]))

    pkgs.pre-commit
    pkgs.ruff

    (pkgs.poetry.override { python3 = pkgs.python311; })
  ];
}
