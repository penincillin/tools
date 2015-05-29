from dbFeature import *


if __name__ == '__main__':
    db = dbFeature()
    l = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
    db.set_data(l,3,2)
    #db.save_to_text_file('r.txt')
    db.save_to_file('r.bin')
    db.read_from_file('r.bin','float')
    print db.get_number()
    print db.get_dim()
    print db.get_data(0,2)
