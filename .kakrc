# See <https://tangled.org/makki.moe/local-kakrc>!

declare-option -hidden str local_root %sh{ pwd -P }

hook -group lsp-filetype-nix global BufSetOption 'filetype=nix' %{
	set-option buffer lsp_servers %exp{
		[nil]
		root = "%opt{local_root}"
		command = "direnv"
		args = ["exec", "%opt{local_root}", "nil"]
		single_instance = false
		settings_section = "_"
		[nil.settings._]
		formatting.command = ["nixfmt"]
	}
}

hook -group lsp-filetype-python global BufSetOption 'filetype=python' %{
	set-option buffer lsp_servers %exp{
		[ruff]
		root = "%opt{local_root}"
		command = "direnv"
		args = ["exec", "%opt{local_root}", "ruff", "server"]
		single_instance = false
		[ty]
		root = "%opt{local_root}"
		command = "direnv"
		args = ["exec", "%opt{local_root}", "ty", "server"]
		single_instance = false
	}
}

hook -group lsp-filetype-shell global BufSetOption 'filetype=sh' %{
	set-option buffer lsp_servers %exp{
		[bash-language-server]
		root = "%opt{local_root}"
		command = "direnv"
		args = ["exec", "%opt{local_root}", "bash-language-server", "start"]
		single_instance = false
	}
}

hook global WinSetOption 'filetype=(nix|python|sh)' lsp-enable-window

evaluate-commands -buffer * -save-regs f %{
	set-register f %opt{filetype}
	set-option buffer filetype ''
	set-option buffer filetype %reg{f}
}
