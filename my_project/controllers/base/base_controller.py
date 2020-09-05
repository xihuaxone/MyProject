from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm.attributes import InstrumentedAttribute

from common.cryptodome import AesCrypt


class ControllerBase(object):
    def __init__(self, table_cls):
        if isinstance(table_cls, DeclarativeMeta):
            table_cls = [table_cls]

        self.table_cls_map = {c.__tablename__: c
                              for c in table_cls}
        self.table_cls_map.update({'default': table_cls[0]})
        self._session = None

    @staticmethod
    def format_return(success, msg='', info=None, **kwargs):
        if not isinstance(success, bool) or not isinstance(msg, str):
            raise Exception('format illegal.')
        ret = {'success': success, 'msg': msg, 'info': info}
        ret.update(kwargs)
        return ret

    def get_table_keys(self, table_name='default'):
        return [c for c, v in self.table_cls_map[table_name].__dict__.items()
                if isinstance(v, InstrumentedAttribute)]

    @property
    def session(self):
        return self._session

    @session.setter
    def session(self, session):
        self._session = session

    @session.getter
    def session(self):
        return self._session

    def commit(self):
        try:
            self.session.commit()
        except Exception as err:
            self.session.rollback()
            raise err
        finally:
            self.session.close()

    def _get(self, filter_dict, table_name='default', **kwargs):
        if not isinstance(filter_dict, dict):
            raise Exception('param filter is not dict.')
        filter_params = []
        for k, v in filter_dict.items():
            k_operator = k.split('.')
            if len(k_operator) == 2:
                k, operator = k_operator
                part_filter = getattr(getattr(self.table_cls_map[table_name], k), operator)(v)
            elif len(k_operator) == 1:
                k = k_operator[0]
                if k.startswith('^'):
                    part_filter = getattr(self.table_cls_map[table_name], k) != v
                else:
                    part_filter = getattr(self.table_cls_map[table_name], k) == v
            else:
                raise Exception('illegal key: [%s]' % k)

            filter_params.append(part_filter)

        query_obj = self._session.query(self.table_cls_map[table_name]).filter(*filter_params)
        query_method = kwargs.get('query_method', 'all')
        info = getattr(query_obj, query_method)()
        if isinstance(info, list):
            info = [i.serialize() for i in info]
        else:
            info = info.serialize() if info else None
        return info

    def _add(self, add_dict, table_name='default'):
        instance = self.table_cls_map[table_name](**add_dict)
        self._session.add(instance)
        return instance.serialize()

    def _update(self, query_dict, update_dict, table_name='default'):
        filter_params = [getattr(self.table_cls_map[table_name], k) == v
                         for k, v in query_dict.items()]

        instance_list = self._session.query(
            self.table_cls_map[table_name]).filter(*filter_params).all()
        for instance in instance_list:
            for k, v in update_dict.items():
                setattr(instance, k, v)

        return [ins.serialize() for ins in instance_list]

    def _delete(self, query_dict, table_name='default'):
        filter_params = [getattr(self.table_cls_map[table_name], k) == v
                         for k, v in query_dict.items()]

        self._session.query(self.table_cls_map[table_name]
                            ).filter(*filter_params).delete()
        return True


    @staticmethod
    def encrypt(string, crypt_type='AES'):
        if crypt_type == 'AES':
            return AesCrypt().encrypt(string)
        else:
            raise Exception('crypt_type not supported')

    @staticmethod
    def decrypt(string, crypt_type='AES'):
        if crypt_type == 'AES':
            return AesCrypt().decrypt(string)
        else:
            raise Exception('crypt_type not supported')
