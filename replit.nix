{ pkgs }: {
  deps = [
    pkgs.xvfb-run
    pkgs.scrot
    pkgs.nmap
    pkgs.geckodriver
    pkgs.replitPackages.prybar-python310
    pkgs.replitPackages.stderred
    pkgs.chromium
    pkgs.chromedriver
  ];
}