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
            if k.endswith('.in_'):
                part_filter = getattr(self.table_cls, k).in_(v)
            elif k.endswith('.like'):
                part_filter = getattr(self.table_cls, k).like(v)
            elif k.endswith('.notin_'):
                part_filter = getattr(self.table_cls, k).notin_(v)
            elif k.endswith('.gt_'):
                part_filter = getattr(self.table_cls, k).gt_(v)
            elif k.endswith('.lt_'):
                part_filter = getattr(self.table_cls, k).lt_(v)
            elif k.endswith('.ge_'):
                part_filter = getattr(self.table_cls, k).ge_(v)
            elif k.endswith('.le_'):
                part_filter = getattr(self.table_cls, k).le_(v)
            else:
                part_filter = getattr(self.table_cls, k) == v

            filter_params.append(part_filter)

        with singleton_session() as session:
            query_obj = session.query(self.table_cls).filter(*filter_params)
            query_method = kwargs.get('query_method', 'all')
            info = getattr(query_obj, query_method)()
            if isinstance(info, list):
                info = [i.dict_format() for i in info]
            else:
                info = info.dict_format()
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

