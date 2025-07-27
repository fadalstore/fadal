{pkgs}: {
  deps = [
    pkgs.haskellPackages.dependent-hashmap
    pkgs.haskellPackages.dependent-sum-template
    pkgs.liferea
    pkgs.python312Packages.pytest-dependency
    pkgs.dependency-track-exporter
    pkgs.dependabot-cli
    pkgs.dependency-track
    pkgs.python313Packages.dependency-injector
    pkgs.rPackages.hydrostats
    pkgs.haskellPackages.dependency
  ];
}
