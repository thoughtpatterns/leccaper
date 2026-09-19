{
  lib,
  python314,
  makeWrapper,
  coreutils,
  dash,
  fdupes,
  ffmpeg,
  gnused,
  src,
}:

python314.pkgs.buildPythonApplication {
  pname = "leccaper";
  version = "0-unstable-2026-09-19";
  inherit src;

  pyproject = true;
  build-system = [ python314.pkgs.uv-build ];

  dependencies = with python314.pkgs; [
    requests
    selenium
    tqdm
  ];

  nativeBuildInputs = [ makeWrapper ];

  postInstall = ''
    install -Dm755 'bin/vf' "$out/bin/vf"
    install -Dm755 'bin/vff' "$out/bin/vff"

    for script in 'vf' 'vff'
    do
      substituteInPlace "$out/bin/$script" --replace-fail '#!/usr/bin/env -S dash -eu' '#!${dash}/bin/dash -eu'
      wrapProgram "$out/bin/$script" --prefix PATH : "$out/bin:${lib.makeBinPath [ coreutils fdupes ffmpeg gnused ]}"
    done
  '';

  pythonImportsCheck = [ "leccaper" ];

  meta = {
    description = "University of Michigan lecture capture download tool";
    homepage = "https://git.sr.ht/~orchid/leccaper";
    license = lib.licenses.agpl3Only;
    maintainers = with lib.maintainers; [ mackeye ];
    mainProgram = "leccaper";
  };
}
