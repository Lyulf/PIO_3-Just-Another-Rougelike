import ui.title_screen
if __name__ == '__main__':
    try:
        game = ui.title_screen.run()
    except SystemExit:
        pass
    except:
        import pdb; pdb.post_mortem()
        raise