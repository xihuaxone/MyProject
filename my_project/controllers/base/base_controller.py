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


class ViewControllerBase(object):
    def __init__(self, table_cls_list):
        self.table_cls_list = table_cls_list
        self.tab_cls_map = {getattr(t_cls, '__tablename__'): t_cls
                            for t_cls in table_cls_list}

    @staticmethod
    def format_return(success, msg, info, **kwargs):
        if not isinstance(success, bool) or not isinstance(msg, str):
            raise Exception('format illegal.')
        ret = {'success': success, 'msg': msg, 'info': info}
        ret.update(kwargs)
        return ret

    def _gen_view(self, session, condition_list):
        # TODO test;
        # condition_list = [{'tab1.id': 'tab2.union_id', 'tab1.user_name': 'tab2.name'}, {'tab2.id': 'tab3.union_id'}]
        _condition_list = []
        ordered_tables = []
        _loop_counter = 0
        while True:
            _loop_counter += 1
            if len(_condition_list) == len(condition_list):
                break
            if _loop_counter >= 10:
                raise Exception('max loop deepth reached, '
                                'some conditions not related with others: %s'
                                % condition_list)

            for condition in condition_list:
                l_tab, r_tab = [i.split('.')[0] for i in condition.popitem()]
                if not _condition_list:
                    ordered_tables.extend([l_tab, r_tab])
                if l_tab in ordered_tables or r_tab in ordered_tables:
                    if condition not in _condition_list:
                        _condition_list.append(condition)
                    ordered_tables.extend([l_tab, r_tab])

            [condition_list.remove(cond)
             for cond in _condition_list if cond in condition_list]

        join_operator = []
        joined_tabs = []
        view = None
        for condition in _condition_list:
            l_cls = r_cls = None
            l_tab = r_tab = None
            for left, right in condition.items():
                l_tab, l_param = left.split('.')
                r_tab, r_param = right.split('.')
                l_cls = self.tab_cls_map.get(l_tab) if not l_cls else l_cls
                r_cls = self.tab_cls_map.get(r_tab) if not r_cls else r_cls
                join_operator.append(getattr(l_cls, l_param) == getattr(r_cls, r_param))

            if not view:
                view = session.query(l_cls)
                joined_tabs.extend([l_tab, r_tab])
            if l_tab not in joined_tabs:
                view = view.join(l_cls, *join_operator)
            elif r_tab not in joined_tabs:
                view = view.join(r_cls, *join_operator)
            else:
                raise Exception('condition not related to '
                                'any other tables: %s' % condition)

            joined_tabs.extend([l_tab, r_tab])

        return view
