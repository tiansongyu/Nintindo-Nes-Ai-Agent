from nes_ai.legacy import forward_legacy_command


def main():
    return forward_legacy_command("train", default_render=False)


if __name__ == "__main__":
    raise SystemExit(main())
