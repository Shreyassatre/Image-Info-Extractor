dl_prompt="""Most Importat: follow mentioned format below strictly. i.e. every character should match same format mentioned below in your response(dont include any * before or after it)
        **don't include** any introductory statement like 'Here is the extracted information' etc.
        All below attributes are case sensetive, that's why I have named all in small case, while providing response you also follow same format.
        DL:
        CLASS:
        EXP:
        LN:
        FN:
        ADDRESS:
        DOB:
        SEX:
        HAIR:
        EYES:
        HGT:
        WGT:
        ISS:
        DD:
        -------------------------------------------------------------

        Here is some additional information about every features format:

        DL:
        note: it is a Driving Licence Number
        label: DL
        contains only uppercase letters, numbers, and special characters like hyphens (-) or spaces.
        Examples and format: F7186359, D5622313, B5221787
        
        CLASS:
        Label: CLASS
        Format: only one cpital latter
        Example: C
        Note: If class not found then assign it default value as "C"
        
        EXP:
        note: if you find any EXP date then extrat it in following format.
        Label: EXP
        Format: MM/DD/YYYY
        Example: 10/25/2022
        if date is in 10/1212012 format then bring it to format by placing / in between them. e.g: 100312005 becomes 10/03/2005
        Correct misdetected characters to /
        
        LN:
        note: It is a last name.
        Label: LN
        Uppercase letters and numbers only

        FN:
        note: It is a first name.
        Label: FN
        Uppercase letters and numbers only

        ADDRESS:
        note: if you find any address then extrat it in following format.
        Format and Example 1: 100 WENDYCT UNION CITY, CA 94587
        Format and Example 1: 29337 CHANCE ST HAYWARD, CA 94544
        
        DOB:
        note: if you find any DOB then extrat it in following format.
        Label: DOB
        Format: MM/DD/YYYY
        Examples: 03/15/1960
        if date is in 10/1212012 format then bring it to format by placing / in between them. e.g: 100312005 becomes 10/03/2005
        Correct misdetected characters to /
        
        SEX:
        note: if you find SEX/Gender then extrat it in following format.
        Label: SEX
        Format: F or M
        Example: M

        HAIR:
        note: if you find HAIR/hair color/type then extrat it in following format.
        Label: HAIR
        Format: Only 3 capital letters.
        Example: BAL, BLK, RED, BLN, BRN

        EYES:
        note: if you find EYES/eyes color then extrat it in following format.
        Label: EYES
        Format: Only 3 capital letters.
        Example: BLK, BLU, BRN

        HGT:
        note: if you find HGT/height then extrat it in following format.
        Label: HGT 
        Example: 5'-08'', 5-08

        WGT:
        note: if you find WGT/weight then extrat it in following format.
        Lable: WGT
        Format: weight in lb
        Example: 240 lb, 400 lb, 160 lb

        ISS:
        note: if you find date at end then consider it as ISS and extrat it in following format.
        Label: ISS
        Format: DD/MM/YYYY
        Example: 06/26/2016

        DD:
        note: it is not only date, it is a date concatinated with some id
        Label: DD
        Example and format: 06/26/2018632B1/CCFD/22"""


id_prompt="""
        Most Importat: follow mentioned format below strictly. i.e. every character should match same format mentioned below in your response(dont include any * before or after it)
        **don't include** any introductory statement like 'Here is the extracted information' etc.
        All below attributes are case sensetive, that's why I have named all in small case, while providing response you also follow same format.
        ID:
        EXP:
        LN:
        FN:
        ADDRESS:
        DOB:
        SEX:
        HAIR:
        EYES:
        HGT:
        WGT:
        ISS:
        DD:
        -------------------------------------------------------------

        Here is some additional information about every features format:

        ID:
        note: it is a ID/Identity Number
        label: ID
        Format:contains only one Coapital letter at start followed by seven numbers.
        Examples and format: N2239816, D3581223, C1924882
        
        EXP:
        note: if you find any EXP date then extrat it in following format.
        Label: EXP
        Format: MM/DD/YYYY
        Example: 10/25/2022
        if date is in 10/1212012 format then bring it to format by placing / in between them. e.g: 100312005 becomes 10/03/2005
        Correct misdetected characters to /
        
        LN:
        note: It is a last name.
        Label: LN
        Format: Uppercase letters and numbers only

        FN:
        note: It is a first name.
        Label: FN
        Format: Uppercase letters and numbers only

        ADDRESS:
        note: if you find any address then extrat it in following format.
        Format and Example 1: 100 WENDYCT UNION CITY, CA 94587
        Format and Example 1: 29337 CHANCE ST HAYWARD, CA 94544
        
        DOB:
        note: if you find any DOB then extrat it in following format.
        Label: DOB
        Format: MM/DD/YYYY
        Examples: 03/15/1960
        if date is in 10/1212012 format then bring it to format by placing / in between them. e.g: 100312005 becomes 10/03/2005
        Correct misdetected characters to /
        
        SEX:
        note: if you find SEX/Gender then extrat it in following format.
        Label: SEX
        Format: F or M
        Example: M

        HAIR:
        note: if you find HAIR/hair color/type then extrat it in following format.
        Label: HAIR
        Format: Only 3 capital letters.
        Example: BAL, BLK, RED, BLN, BRN

        EYES:
        note: if you find EYES/eyes color then extrat it in following format.
        Label: EYES
        Format: Only 3 capital letters.
        Example: BLK, BLU, BRN

        HGT:
        note: if you find HGT/height then extrat it in following format.
        Label: HGT 
        Example: 5'-08'', 5-08

        WGT:
        note: if you find WGT/weight then extrat it in following format.
        Lable: WGT
        Format: weight in lb
        Example: 240 lb, 400 lb, 160 lb

        ISS:
        note: if you find date at end then consider it as ISS and extrat it in following format.
        Label: ISS
        Format: DD/MM/YYYY
        Example: 06/26/2016

        DD:
        note: it is not only date, it is a date concatinated with some id
        Label: DD
        Example and format: 06/26/2018632B1/CCFD/22
"""

passport_prompt="""
        I am extracting information from passport and it has some spanish words. If you don't find english label then try to make sense out of spanish word.
        Most Importat: follow mentioned format below strictly. i.e. every character should match same format mentioned below in your response(dont include any * before or after it)
        **don't include** any introductory statement like 'Here is the extracted information' etc.
        All below attributes are case sensetive, that's why I have named all in small case, while providing response you also follow same format.
        Type:
        Issuing state code:
        Passport No:
        Surname:
        Given names:
        Nationality:
        Date of birth:
        Personal No:
        Sex:
        Place of birth:
        Issue date:
        Expiry date:
        Authority:
        -------------------------------------------------------------

        Here is some additional information about every features format:

        Type:
        note: if you find any Type then extrat it in following format.
        Format: Single capital letter
        Example: P

        Issuing state code:
        note: if you find any Issuing state code then extrat it in following format.
        Format: Three capital letters.
        Example: MEX

        Passport No:
        note: if you find any Passport Number then extrat it in following format.
        Format and example: E13837577

        Surname:
        note: if you find any Surname then extrat it in following format.
        Format: Mostly a Spanish name.
        Example: VELAZQUEZ LIMON

        Given names:
        note: if you find any Given names then extrat it in following format.
        Format: Mostly a spanish name
        Example: VICENTE CARLOS

        Nationality:
        note: if you find any Nationality then extrat it in following format.
        Example: MEXICANA

        Date of birth:
        note: if you find any Date of birth then extrat it in following format.
        Label: Date of birth
        Format: MM/DD/YYYY
        if date is in 10/1212012 format then bring it to format by placing / in between them. e.g: 100312005 becomes 10/03/2005
        Correct misdetected characters to /

        Personal No:
        note: if you find any Personal number then extrat it in following format.
        Example and format: VELV791228HJCLMC09

        Sex:
        note: if you find SEX/Gender then extrat it in following format.
        Label: Sex
        Format: F or M
        Example: M

        Place of birth:
        note: if you find any Place of birth then extrat it in following format.
        Example and format: GUADALAJARA, JAL. ,MEX

        Issue date:
        note: if you find any Issue date after Authority then extrat it in following format.
        Label: Issue date
        if date is in 10/1212012 format then bring it to format by placing / in between them. e.g: 100312005 becomes 10/03/2005
        Correct misdetected characters to /

        Expiry date:
        note: if you find any Expiry date then extrat it in following format.
        Label: Expiry date
        if date is in 10/1212012 format then bring it to format by placing / in between them. e.g: 100312005 becomes 10/03/2005
        Correct misdetected characters to /
        
        Authority:
        note: if you find any Authority name then extrat it in following format.
        Label: Authority

"""




