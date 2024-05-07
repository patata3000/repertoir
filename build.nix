with import <nixpkgs> {};
with pkgs.python312Packages;
  buildPythonPackage rec {
    name = "repertoir";
    src = ./.;
    pyproject = true;
    nativeBuildInputs = [poetry-core];
    # format = "pyproject";
    buildInputs = [click yt-dlp];
  }
