with (import <nixpkgs> {});
mkShell {
	buildInputs = [
		pkgs.python3
	];
}