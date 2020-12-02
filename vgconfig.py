cache_name = "vgmusic_downloads"
debug_print = True

def verify(): # to preserve what I did before
    pass

if __name__ == "__main__":
    try:
        verify()
        print("This file is configured correctly!")
    except AssertionError as e:
        print("Failed to verify.")
        print(str(e))

