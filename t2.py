for i in range(len(tables[int(chosen_table)]["seats"])):
    if tables[int(chosen_table)]["seats"][i]["name"] is not None:
        if int(tables[int(chosen_table)]["seats"][i]["result"][0]) > 21:
            tables[int(chosen_table)]["seats"][i]["wlp"] = "loss"
            db.update_user_score(tables[int(chosen_table)]["seats"][i]["name"],
                                 "-" + tables[int(chosen_table)]["seats"][i]["bet"])
            db.update_win_loss_push(tables[int(chosen_table)]["seats"][i]["name"],
                                    tables[int(chosen_table)]["seats"][i]["wlp"])
        elif int(tables[int(chosen_table)]["dealer"]["result"][0]) > 21 or int(
                tables[int(chosen_table)]["seats"][i]["result"][0]) > int(
                tables[int(chosen_table)]["dealer"]["result"][0]):
            tables[int(chosen_table)]["seats"][i]["wlp"] = "win"
            if int(tables[int(chosen_table)]["seats"][i]["result"][0]) == 21 and len(
                    tables[int(chosen_table)]["seats"][i]["cards"]) == 2:
                db.update_user_score(tables[int(chosen_table)]["seats"][i]["name"],
                                     str(int(tables[int(chosen_table)]["seats"][i]["bet"]) * 3 / 2))
                db.update_win_loss_push(tables[int(chosen_table)]["seats"][i]["name"],
                                        tables[int(chosen_table)]["seats"][i]["wlp"])
            else:
                db.update_user_score(tables[int(chosen_table)]["seats"][i]["name"],
                                     tables[int(chosen_table)]["seats"][i]["bet"])
                db.update_win_loss_push(tables[int(chosen_table)]["seats"][i]["name"],
                                        tables[int(chosen_table)]["seats"][i]["wlp"])
        elif int(tables[int(chosen_table)]["seats"][i]["result"][0]) == int(
                tables[int(chosen_table)]["dealer"]["result"][0]):
            tables[int(chosen_table)]["seats"][i]["wlp"] = "push"
            db.update_win_loss_push(tables[int(chosen_table)]["seats"][i]["name"],
                                    tables[int(chosen_table)]["seats"][i]["wlp"])
        else:
            tables[int(chosen_table)]["seats"][i]["wlp"] = "loss"
            db.update_user_score(tables[int(chosen_table)]["seats"][i]["name"],
                                 "-" + tables[int(chosen_table)]["seats"][i]["bet"])
            db.update_win_loss_push(tables[int(chosen_table)]["seats"][i]["name"],
                                    tables[int(chosen_table)]["seats"][i]["wlp"])
        build_and_send_message(all_table_players[int(chosen_table)][tables[int(chosen_table)]["seats"][i]["name"]],
                               PROTOCOL_SERVER['leaderboard_ok'],
                               str(db.get_user_info(tables[int(chosen_table)]["seats"][i]["name"])))
