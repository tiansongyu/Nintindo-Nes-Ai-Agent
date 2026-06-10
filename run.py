from nes_ai.legacy import forward_legacy_command


def main():
    return forward_legacy_command("play", default_render=True)


if __name__ == "__main__":
    raise SystemExit(main())
