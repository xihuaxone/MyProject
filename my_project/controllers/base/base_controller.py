from models.base.base import singleton_session


class ControllerBase(object):
    def __init__(self, table_cls):
        self.table_cls = table_cls

    @staticmethod
    def format_return(success, msg, info, **kwargs):
        if not isinstance(success, bool) or not isinstance(msg, str):
            raise Exception('format illegal.')
        ret = {'success': success, 'msg': msg, 'info': info}
        ret.update(kwargs)
        return ret

    def _get(self, filter_dict, **kwargs):
        if not isinstance(filter_dict, dict):
            raise Exception('param filter is not dict.')
        filter_params = []
        for k, v in filter_dict.items():
            k_operator = k.split('.')
            if len(k_operator) == 2:
                k, operator = k_operator
                part_filter = getattr(getattr(self.table_cls, k), operator)(v)
            elif len(k_operator) == 1:
                k = k_operator[0]
                if k.startswith('^'):
                    part_filter = getattr(self.table_cls, k) != v
                else:
                    part_filter = getattr(self.table_cls, k) == v
            else:
                raise Exception('illegal key: [%s]' % k)

            filter_params.append(part_filter)

        with singleton_session() as session:
            query_obj = session.query(self.table_cls).filter(*filter_params)
            query_method = kwargs.get('query_method', 'all')
            info = getattr(query_obj, query_method)()
            if isinstance(info, list):
                info = [i.dict_format() for i in info]
            else:
                info = info.dict_format() if info else None
            return info

    def _add(self, add_dict):
        with singleton_session() as session:
            instance = self.table_cls(**add_dict)
            session.add(instance)
        return instance.dict_format()

    def _update(self, query_dict, update_dict):
        with singleton_session() as session:
            filter_params = [getattr(self.table_cls, k) == v
                             for k, v in query_dict.items()]

            instance_list = session.query(
                self.table_cls).filter(*filter_params).all()
            for instance in instance_list:
                for k, v in update_dict.items():
                    setattr(instance, k, v)

        return [ins.dict_format() for ins in instance_list]

