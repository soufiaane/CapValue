from test import spf_check_task
from celery.result import AsyncResult
from test import new_spf_check

i = 1
files = ["com (2).txt", "com (3).txt", "com (4).txt", "com (5).txt", "com (6).txt", "com (7).txt",
         "com (8).txt", "com (9).txt", "com (10).txt", "com (11).txt", "com (12).txt", "com (13).txt", "com (14).txt",
         "com (15).txt", "com (16).txt", "com (17).txt", "com (18).txt", "com (19).txt", "com (20).txt", "com (21).txt",
         "com (22).txt", "com (23).txt", "com (24).txt", "com (25).txt", "com (26).txt", "com (27).txt", "com (28).txt",
         "com (29).txt", "com (30).txt", "com (31).txt", "com (32).txt", "com (33).txt", "com (34).txt", "com (35).txt",
         "com (36).txt", "com (37).txt", "com (38).txt", "com (39).txt", "com (40).txt", "com (41).txt", "com (42).txt",
         "com (43).txt", "com (44).txt", "com (45).txt", "com (46).txt", "com (47).txt", "com (48).txt", "com (49).txt",
         "com (50).txt", "com (51).txt", "com (52).txt", "com (53).txt", "com (54).txt", "com (55).txt", "com (56).txt",
         "com (57).txt", "com (58).txt", "com (59).txt", "com (60).txt", "com (61).txt", "com (62).txt", "com (63).txt",
         "com (64).txt", "com (65).txt", "com (66).txt", "com (67).txt", "com (68).txt", "com (69).txt", "com (70).txt",
         "com (71).txt", "com (72).txt", "com (73).txt", "com (74).txt", "com (75).txt", "com (76).txt", "com (77).txt",
         "com (78).txt", "com (79).txt", "com (80).txt", "com (81).txt", "com (82).txt", "com (83).txt", "com (84).txt",
         "com (85).txt", "com (86).txt", "com (87).txt", "com (88).txt", "com (89).txt", "com (90).txt", "com (91).txt",
         "com (92).txt", "com (93).txt", "com (94).txt", "com (95).txt", "com (96).txt", "com (97).txt", "com (98).txt",
         "com (99).txt", "com (100).txt", "com (101).txt", "com (102).txt", "com (103).txt", "com (104).txt",
         "com (105).txt", "com (106).txt", "com (107).txt", "com (108).txt", "com (109).txt", "com (110).txt",
         "com (111).txt", "com (112).txt", "com (113).txt", "com (114).txt", "com (115).txt", "com (116).txt",
         "com (117).txt", "com (118).txt", "com (119).txt", "com (120).txt", "com (121).txt", "com (122).txt",
         "com (123).txt", "com (124).txt", "com (125).txt", "info (1).txt", "info (2).txt", "info (3).txt",
         "info (4).txt", "info (5).txt", "info (6).txt", "net (1).txt", "net (2).txt", "net (3).txt", "net (4).txt",
         "net (5).txt", "net (6).txt", "net (7).txt", "net (8).txt", "net (9).txt", "net (10).txt", "net (11).txt",
         "net (12).txt", "net (13).txt", "net (14).txt", "net (15).txt", "net (16).txt", "org (1).txt", "org (2).txt",
         "org (3).txt", "org (4).txt", "org (5).txt", "org (6).txt", "org (7).txt", "org (8).txt", "org (9).txt",
         "org (10).txt", "org (11).txt", "us (1).txt", "us (2).txt"]

for file in files:
    with open("Mahmoud\\" + file, 'r') as f:
        for domain in f:
            spf_task = spf_check_task.apply_async((str(i), domain.replace("\n", "")), queue="SPF63")
            task_file_id = open("Mahmoud\\results\\" + file.replace(".txt", "") + "_result_spf_file_id.txt", 'a')
            task_file_id.write("%s;%s\n" % (str(i), spf_task.id))
            task_file_id.close()
            i += 1
