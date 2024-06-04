import pandas as pd


def TestData01():
    "When find all partners"
    print("\n FIND ALL \n")
    df = pd.DataFrame({
            "id": [1,2,3,4],
            "name": ['A', 'B','C', 'D'],
            "lastName": ['A', 'B','C', 'D'],
            "age": [18, 20, 22, 24],
            "sex": ['Мужской','Мужской','Мужской','Мужской'],
            "city": ['Москва','Москва','Москва','Москва'],
            "runLevel": ['Новичок', 'Новичок', 'Новичок', 'Новичок'],
            "accountLink": ['Link', 'Link', 'Link', 'Link'],
            "levelPartnerNeed": [False, False, False, False],
            "anyGender": [True, True, True, True],
            "chooseOldPartner": [True, True, True, True],
            "meetActive": [True, True, True, True],
            "idTelegram": [1, 2, 3, 4],
            "linkTelegram": [1, 2, 3, 4],
        }
    )
    partners = pd.DataFrame(columns=["id"])
    return df , partners


def TestData02():
    "When find 2 partners and one is not"
    print("\n NOT FIND ALL \n")
    df = pd.DataFrame({
            "id": [1,2,3,],
            "name": ['A', 'B','C',],
            "lastName": ['A', 'B','C',],
            "age": [18, 20, 22,],
            "sex": ['Мужской','Мужской','Мужской',],
            "city": ['Москва','Москва','Москва',],
            "runLevel": ['Новичок', 'Новичок', 'Новичок',],
            "accountLink": ['Link', 'Link', 'Link',],
            "levelPartnerNeed": [False, False, False,],
            "anyGender": [True, True, True,],
            "chooseOldPartner": [True, True, True,],
            "meetActive": [True, True, True,],
            "idTelegram": [1, 2, 3,],
            "linkTelegram": [1, 2, 3,],
        }
    )
    partners = pd.DataFrame(columns=["id"])
    return df , partners


def TestData03():
    "When find 2 partners and two is not because of gender"
    print("\n NOT FIND ALL \n")
    df = pd.DataFrame({
            "id": [1,2,3,4],
            "name": ['A', 'B','C', 'D'],
            "lastName": ['A', 'B','C', 'D'],
            "age": [18, 20, 22, 24],
            "sex": ['Мужской','Мужской','Мужской','Женский'],
            "city": ['Москва','Москва','Москва','Москва'],
            "runLevel": ['Новичок', 'Новичок', 'Новичок', 'Новичок'],
            "accountLink": ['Link', 'Link', 'Link', 'Link'],
            "levelPartnerNeed": [False, False, False, False],
            "anyGender": [True, True, True, False],
            "chooseOldPartner": [True, True, True, True],
            "meetActive": [True, True, True, True],
            "idTelegram": [1, 2, 3, 4],
            "linkTelegram": [1, 2, 3, 4],
        }
    )
    partners = pd.DataFrame(columns=["id"])
    return df , partners


def TestData04():
    "When find 2 partners and two is not because of age"
    print("\n NOT FIND ALL \n")
    df = pd.DataFrame({
            "id": [1,2,3,4],
            "name": ['A', 'B','C', 'D'],
            "lastName": ['A', 'B','C', 'D'],
            "age": [18, 20, 22, 36],
            "sex": ['Мужской','Мужской','Мужской','Мужской'],
            "city": ['Москва','Москва','Москва','Москва'],
            "runLevel": ['Новичок', 'Новичок', 'Новичок', 'Новичок'],
            "accountLink": ['Link', 'Link', 'Link', 'Link'],
            "levelPartnerNeed": [False, False, False, False],
            "anyGender": [True, True, True, True],
            "chooseOldPartner": [True, True, True, True],
            "meetActive": [True, True, True, True],
            "idTelegram": [1, 2, 3, 4],
            "linkTelegram": [1, 2, 3, 4],
        }
    )
    partners = pd.DataFrame(columns=["id"])
    return df , partners


def TestData05():
    "When find 2 partners and two is not because of run level"
    print("\n NOT FIND ALL \n")
    df = pd.DataFrame({
            "id": [1,2,3,4],
            "name": ['A', 'B','C', 'D'],
            "lastName": ['A', 'B','C', 'D'],
            "age": [18, 20, 22, 24],
            "sex": ['Мужской','Мужской','Мужской','Мужской'],
            "city": ['Москва','Москва','Москва','Москва'],
            "runLevel": ['Новичок', 'Новичок', 'Новичок', 'Любитель'],
            "accountLink": ['Link', 'Link', 'Link', 'Link'],
            "levelPartnerNeed": [False, False, False, True],
            "anyGender": [True, True, True, True],
            "chooseOldPartner": [True, True, True, True],
            "meetActive": [True, True, True, True],
            "idTelegram": [1, 2, 3, 4],
            "linkTelegram": [1, 2, 3, 4],
        }
    )
    partners = pd.DataFrame(columns=["id"])
    return df , partners


def TestData06():
    "When find 2 partners and two the same"

    df = pd.DataFrame({
            "id": [1,2,3,4],
            "name": ['A', 'B','C', 'D'],
            "lastName": ['A', 'B','C', 'D'],
            "age": [18, 20, 22, 24],
            "sex": ['Мужской','Мужской','Мужской','Женский'],
            "city": ['Москва','Москва','Москва','Москва'],
            "runLevel": ['Новичок', 'Новичок', 'Новичок', 'Новичок'],
            "accountLink": ['Link', 'Link', 'Link', 'Link'],
            "levelPartnerNeed": [False, False, False, False],
            "anyGender": [True, True, True, True],
            "chooseOldPartner": [True, True, True, True],
            "meetActive": [True, True, True, True],
            "idTelegram": [1, 2, 3, 4],
            "linkTelegram": [1, 2, 3, 4],
        }
    )
    partners = pd.DataFrame(columns=["id"])
    return df , partners


def TestData07():
    "When find 2 partners and two the same"

    df = pd.DataFrame({
            "id": [1,2,3,4],
            "name": ['A', 'B','C', 'D'],
            "lastName": ['A', 'B','C', 'D'],
            "age": [18, 20, 22, 24],
            "sex": ['Мужской','Мужской','Мужской','Женский'],
            "city": ['Москва','Москва','Москва','Москва'],
            "runLevel": ['Новичок', 'Новичок', 'Новичок', 'Новичок'],
            "accountLink": ['Link', 'Link', 'Link', 'Link'],
            "levelPartnerNeed": [False, False, False, False],
            "anyGender": [True, True, True, True],
            "chooseOldPartner": [True, True, True, True],
            "meetActive": [True, True, True, True],
            "idTelegram": [1, 2, 3, 4],
            "linkTelegram": [1, 2, 3, 4],
        }
    )
    partners = pd.DataFrame(columns=["id"])
    return df , partners