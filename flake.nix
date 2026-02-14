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
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = import nixpkgs { inherit system; };
        python = pkgs.python314;
      in
      {
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
