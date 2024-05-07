# shell.nix
let
  # We pin to a specific nixpkgs commit for reproducibility.
  # Last updated: 2024-04-29. Check for new commits at https://status.nixos.org.
  pkgs = import (fetchTarball "https://github.com/NixOS/nixpkgs/archive/ad7efee13e0d216bf29992311536fce1d3eefbef.tar.gz") {};
in
  pkgs.mkShell {
    packages = [
      (pkgs.python312.withPackages (python-pkgs: [
        # select Python packages here
        # These packages are available for testing the python app.
        python-pkgs.black
        python-pkgs.click
        python-pkgs.yt-dlp
      ]))
    ];
  }
