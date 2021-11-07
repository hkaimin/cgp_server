#!/usr/bin/env python'
# -*- coding: utf-8 -*-

from flask import jsonify, request, current_app as app
from flask.ext.admin import expose, BaseView

class MapEditorView(BaseView):

    def is_visible(self):
        return False

    def resource_db(self):
        zoning = app.extensions['zoning']
        return zoning.my_resource_db()

    def get_all_maps(self):
        db = self.resource_db()
        return list(db['map'].find())

    def get_map(self, map_id):
        db = self.resource_db()
        return db['map'].find_one({'_id': map_id})

    def get_map_tiles(self, map_id):
        db = self.resource_db()
        return list(db['tile'].find({'mid': map_id}))

    def get_all_buildings(self):
        db = self.resource_db()
        return list(db['buildings'].find())

    def remove_map_tiles(self, map_id):
        db = self.resource_db()
        return db['tile'].remove({'mid': map_id})

    def gen_tile_pk(self):
        db = self.resource_db()
        docs = list(db['tile'].find().sort('_id', -1).limit(1))
        if docs:
            return docs[0]['_id'] + 1
        else:
            return 1

    def update_map_tiles(self, map_id, map, tiles):
        db = self.resource_db()
        db['map'].update({'_id': map_id}, { '$set':
            {
                'mapSize': map['mapSize'],
            }
        })
        tile_pk = self.gen_tile_pk()
        for i, tile in enumerate(tiles):
            tile['mid'] = map_id
            tile['_id'] = tile_pk + i
        self.remove_map_tiles(map_id)
        if tiles:
            db['tile'].insert(tiles)
        return True

    # 页面 #

    @expose('/', methods=('GET', 'POST'))
    def index(self):
        return self.render('mapeditor/layout.html')

    @expose('/map/', methods=('GET', ))
    def map_list(self):
        result = dict(maps=self.get_all_maps())
        return jsonify(result)

    @expose('/map/<int:id>', methods=('GET', 'POST'))
    def map(self, id):
        if request.method == 'POST':
            map = request.json['map']
            tiles = request.json['tiles']
            success = self.update_map_tiles(id, map, tiles)
            result = dict(success=success)
            return jsonify(result)

        map = self.get_map(id)
        tiles = self.get_map_tiles(id)
        result = dict(map=map, tiles=tiles)
        return jsonify(result)

    @expose('/building/', methods=('GET', ))
    def building(self):
        result = dict(buildings=self.get_all_buildings())
        return jsonify(result)
