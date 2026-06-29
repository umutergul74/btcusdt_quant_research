from btc_quant.cli import main

if __name__ == '__main__':
    raise SystemExit(main(['package-phase1', *(__import__('sys').argv[1:])]))
