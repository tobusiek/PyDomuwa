# def create_game_room(
#     game: schemas.GameRoomCreateSchema,
#     db_sess: Session = Depends(db.get_db_session),
# ) -> models.GameRoom:
#     db_game_room = models.GameRoom(
#         game_name=game.game_name,
#         game_category=game.game_category,
#         players=[],
#     )
#     return db.save_obj(db_game_room, db_sess)
#
#
# def add_player(
#     game_room_id: int,
#     player_id: int,
#     db_sess: Session = Depends(db.get_db_session),
# ) -> models.GameRoom:
#     player = db.get_obj_of_type_by_id(player_id, models.Player, "Player", db_sess)
#     game_room = db.get_obj_of_type_by_id(
#         game_room_id,
#         models.GameRoom,
#         "GameRoom",
#         db_sess,
#     )
#     player.game_room = game_room
#     player.game_room_id = game_room_id
#     if player not in game_room.players:
#         db.save_obj(player, db_sess)
#         game_room.players.append(player)
#     return db.save_obj(game_room, db_sess)
#
#
# def remove_player(
#     game_room_id: int,
#     player_id: int,
#     db_sess: Session = Depends(db.get_db_session),
# ) -> models.GameRoom:
#     player = db.get_obj_of_type_by_id(player_id, models.Player, "Player", db_sess)
#     player.game_room = None
#     player.game_room_id = None
#     db.save_obj(player, db_sess)
#     game = db.get_obj_of_type_by_id(
#         game_room_id,
#         models.GameRoom,
#         "GameRoom",
#         db_sess,
#     )
#     game.players.remove(player)
#     return db.save_obj(game, db_sess)
#
#
# def remove_all_players(
#     game_room_id: int,
#     db_sess: Session = Depends(db.get_db_session),
# ) -> models.GameRoom:
#     game = db.get_obj_of_type_by_id(
#         game_room_id,
#         models.GameRoom,
#         "GameRoom",
#         db_sess,
#     )
#     players = (
#         db_sess.query(models.Player)
#         .filter(models.Player.game_room_id == game_room_id)
#         .all()
#     )
#     for player in players:
#         players_services.reset_player_game_room(player.id, db_sess)
#     return db.save_obj(game, db_sess)
#
#
# def delete_game_room(
#     game_room_id: int,
#     db_sess: Session = Depends(db.get_db_session),
# ) -> None:
#     db.delete_obj(game_room_id, models.GameRoom, "GameRoom", db_sess)
#     players = (
#         db_sess.query(models.Player)
#         .filter(models.Player.game_room_id == game_room_id)
#         .all()
#     )
#     for player in players:
#         players_services.reset_player_game_room(player.id, db_sess)
