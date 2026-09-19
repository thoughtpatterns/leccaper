{
  description = "Developer shell";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs =
    {
      self,
      nixpkgs,
      flake-utils,
    }:
    {
      overlays.default = final: _: {
        leccaper = self.packages.${final.stdenv.hostPlatform.system}.leccaper;
      };
    }
    // flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = import nixpkgs { inherit system; };
        python = pkgs.python314;
      in
      {
        packages = rec {
          default = leccaper;
          leccaper = pkgs.callPackage ./package.nix { src = self; };
        };

        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            dash
            fdupes
            ffmpeg
            python
            uv
          ];

          shellHook = ''
            if ! [ -d .venv ]
            then uv venv -p '${python}/bin/python'
            fi

            unset VIRTUAL_ENV
            . .venv/bin/activate

            export PATH="$(realpath ./bin):$PATH"
          '';
        };
      }
    );
}
