from storage import Storage

def main(base: str):
    Storage.initialize(base, 'server')
    Storage.initialize(base, 'client')
    Storage.initialize(base, 'ccc')

if __name__ == '__main__':
    main('precios_fce_unpsjb')
