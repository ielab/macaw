"""
The naive output post processing unit.

Authors: Hamed Zamani (hazamani@microsoft.com)
"""

from macaw import util
from macaw.core.output_handler.output_selection import OutputProcessing
from macaw.core.interaction_handler.msg import Message


class NaiveOutputProcessing(OutputProcessing):
    def __init__(self, params):
        """
        This module simply prioritizes the action outputs. If the message was a command, it returns the command's
        output. Otherwise, it prioritizes QA results and then retrieval results (the rational is that if there is an
        exact answer for the user's question, there is no need to show the retrieval results).

        Args:
            params(dict): A dict of parameters.
        """
        super().__init__(params)

    def output_selection(self, conv_list, candidate_outputs):
        """
        This method selects one of the outputs produced by the actions.

        Args:
            conv_list(list): List of util.msg.Message, each corresponding to a conversational message from / to the
            user. This list is in reverse order, meaning that the first elements is the last interaction made by user.
            candidate_outputs(dict): A dict of str (i.e., action) to list of Documents (i.e., the action's result) as
            the response. This dict is produced by action dispatcher, which means this is the aggregation of all the
            executed actions.

        Returns:
            A str denoting the selected action. If none is selected, None is returned.
        """
        if '#get_doc' in candidate_outputs:
            return '#get_doc'
        if 'qa' in candidate_outputs:
            if len(candidate_outputs['qa'][0].text) > 0:
                if conv_list[0].text.endswith('?') \
                        or conv_list[0].text.lower().startswith('what') \
                        or conv_list[0].text.lower().startswith('who') \
                        or conv_list[0].text.lower().startswith('when') \
                        or conv_list[0].text.lower().startswith('where') \
                        or conv_list[0].text.lower().startswith('how'):
                    return 'qa'
        if 'retrieval' in candidate_outputs:
            if len(candidate_outputs['retrieval']) > 0:
                return 'retrieval'
        return None

    def get_output(self, conv, candidate_outputs):
        """
        The response Message generation method.

        Args:
            conv_list(list): List of util.msg.Message, each corresponding to a conversational message from / to the
            user. This list is in reverse order, meaning that the first elements is the last interaction made by user.
            candidate_outputs(dict): A dict of str (i.e., action) to list of Documents (i.e., the action's result) as
            the response. This dict is produced by action dispatcher, which means this is the aggregation of all the
            executed actions.

        Returns:
            A response Message to be sent to the user.
        """
        user_id = conv[0].user_id
        user_info = conv[0].user_info
        msg_info = dict()
        msg_info['msg_id'] = conv[0].msg_info['msg_id']
        msg_info['msg_source'] = 'system'
        text = ''
        user_interface = conv[0].user_interface

        selected_action = self.output_selection(conv, candidate_outputs)
        if selected_action is None:
            msg_info['msg_type'] = 'text'
            msg_info['msg_creator'] = 'no answer error'
            text = 'No response has been found! Please try again!'
        elif selected_action == 'qa':
            msg_info['msg_type'] = conv[0].msg_info['msg_type']
            msg_info['msg_creator'] = 'qa'
            text = f'{candidate_outputs["qa"][0].text}\nSource: {candidate_outputs["qa"][0].web_url}'
        elif selected_action == 'retrieval':
            msg_info['msg_type'] = 'options'
            msg_info['msg_creator'] = 'retrieval'
            text = 'Retrieved document list (click to see the document content):'
            msg_info['options'] = [(output.text, '#get_doc ' + output.id, output.score, output.web_url) for output in candidate_outputs['retrieval']]
        elif selected_action == '#get_doc':
            msg_info['msg_type'] = 'text'
            msg_info['msg_creator'] = '#get_doc'
            text = f'{candidate_outputs["#get_doc"][0].title}\n{candidate_outputs["#get_doc"][0].text}\nSource: {candidate_outputs["#get_doc"][0].web_url}'
        else:
            raise Exception('The candidate output key is not familiar!')
        timestamp = util.current_time_in_milliseconds()
        if timestamp <= conv[0].timestamp:
            raise Exception('There is a problem in the output timestamp!')
        return Message(user_interface, user_id, user_info, msg_info, text, timestamp)