# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from . import URLBuilder


class Customers(URLBuilder):
    client = None

    def __init__(self, client):
        self.client = client

    def get_customers_by_action(self, recipient_group_id, action_id, date, attributes=None, delimiter=';'):
        """Returns the list of customer IDs associated with a particular recipient group and action on
        a particular date, plus an optional customer attribute."""
        if not recipient_group_id or not action_id or not date:
            raise Exception('No RecipientGroupID, ActionID and Date provided')

        data = {
            'RecipientGroupID': recipient_group_id,
            'ActionID': action_id,
            'Date': date
        }

        if attributes and type(attributes) == type(list):
            attributes = ';'.join(attributes)
            data['CustomerAttributes'] = attributes

            if delimiter:
                if delimiter in self.AUTHORIZED_DELIMITERS and delimiter not in self.UNAUTHORIZED_DELIMITERS:
                    data['CustomerAttributesDelimiter'] = delimiter
                else:
                    raise Exception('Invalid delimiter')

        response = self.client.get(self._get_url(), data)
        if not response:
            return False

        results = list()
        for item in response.json():
            result = {
                'customer_id': item['CustomerID']
            }
            if attributes:
                customer_attributes = item['CustomerAttributes'].split(delimiter)
                for index, attribute in enumerate(attributes):
                    result['attributes'][attribute] = customer_attributes[index]
            results.append(result)

        return results

    def get_customer_actions_by_target_group(self, target_group_id, date,
                                             include_control_group=False, attributes=None, delimiter=';'):
        """Returns a list of customers and the details of the marketing actions they received, for a
        particular target group ID on a particular date."""
        if not target_group_id or not date:
            raise Exception('No TargetGroupID and Date provided')

        data = {
            'TargetGroupId': target_group_id,
            'Date': date
        }

        if include_control_group:
            data['IncludeControlGroup'] = True

        if attributes and type(attributes) == type(list):
            attributes = ';'.join(attributes)
            data['CustomerAttributes'] = attributes

            if delimiter:
                if delimiter in self.AUTHORIZED_DELIMITERS and delimiter not in self.UNAUTHORIZED_DELIMITERS:
                    data['CustomerAttributesDelimiter'] = delimiter
                else:
                    raise Exception('Invalid delimiter')

        response = self.client.get(self._get_url(), data)
        if not response:
            return False

        results = list()
        for item in response.json():
            result = {
                'customer_id': item['CustomerID'],
                'action_id': item['ActionID'],
                'channel_id': item['ChannelID']
            }
            if attributes:
                customer_attributes = item['CustomerAttributes'].split(delimiter)
                for index, attribute in enumerate(attributes):
                    result['attributes'][attribute] = customer_attributes[index]
            results.append(result)

        return results

    def get_customer_one_time_actions_by_date(self, date,
                                              include_control_group=False, attributes=None, delimiter=';'):
        """Returns a list of customers and the details of the marketing actions they received as part of one-time
        campaigns executed on a particular date."""
        if not date:
            raise Exception('No Date provided')

        data = {
            'Date': date
        }

        if include_control_group:
            data['IncludeControlGroup'] = True

        if attributes and type(attributes) == type(list):
            attributes = ';'.join(attributes)
            data['CustomerAttributes'] = attributes

            if delimiter:
                if delimiter in self.AUTHORIZED_DELIMITERS and delimiter not in self.UNAUTHORIZED_DELIMITERS:
                    data['CustomerAttributesDelimiter'] = delimiter
                else:
                    raise Exception('Invalid delimiter')

        response = self.client.get(self._get_url(), data)
        if not response:
            return False

        results = list()
        for item in response.json():
            result = {
                'customer_id': item['CustomerID'],
                'action_id': item['ActionID'],
                'channel_id': item['ChannelID']
            }
            if attributes:
                customer_attributes = item['CustomerAttributes'].split(delimiter)
                for index, attribute in enumerate(attributes):
                    result['attributes'][attribute] = customer_attributes[index]
            results.append(result)

        return results

    def get_target_group_changers(self, start_date, end_date,
                                  customer_id=None, initial_target_group_id=None, final_target_group_id=None,
                                  attributes=None, delimiter=';'):
        """Returns the before and after target group IDs for customers whose target group changed during a particular
        date range."""
        if not start_date or not end_date:
            raise Exception('No StartDate and EndDate provided')

        data = {
            'StartDate': start_date,
            'EndDate': end_date
        }

        if customer_id:
            data['CustomerID'] = customer_id

        if initial_target_group_id:
            data['InitialTargetGroupID'] = initial_target_group_id

        if final_target_group_id:
            data['FinalTargetGroupID'] = final_target_group_id

        if attributes and type(attributes) == type(list):
            attributes = ';'.join(attributes)
            data['CustomerAttributes'] = attributes

            if delimiter:
                if delimiter in self.AUTHORIZED_DELIMITERS and delimiter not in self.UNAUTHORIZED_DELIMITERS:
                    data['CustomerAttributesDelimiter'] = delimiter
                else:
                    raise Exception('Invalid delimiter')

        response = self.client.get(self._get_url(), data)
        if not response:
            return False

        results = list()
        for item in response.json():
            result = {
                'customer_id': item['CustomerID'],
                'initial_target_group_id': item['InitialTargetGroupID'],
                'final_target_group_id': item['FinalTargetGroupID']
            }
            if attributes:
                customer_attributes = item['CustomerAttributes'].split(delimiter)
                for index, attribute in enumerate(attributes):
                    result['attributes'][attribute] = customer_attributes[index]
            results.append(result)

        return results

    def get_cusomer_attribute_changers(self, start_date, end_date, changed_customer_attribute,
                                       attributes=None, delimiter=';'):
        """Returns an array of customer IDs, and their before and after attribute values, for customers whose selected
        attribute changed during a particular date range."""
        if not start_date or not end_date or not changed_customer_attribute:
            raise Exception('No StartDate, EndDate and ChangedCustomerAttribute provided')

        data = {
            'StartDate': start_date,
            'EndDate': end_date,
            'ChangedCustomerAttribute': changed_customer_attribute
        }

        if attributes and type(attributes) == type(list):
            attributes = ';'.join(attributes)
            data['CustomerAttributes'] = attributes

            if delimiter:
                if delimiter in self.AUTHORIZED_DELIMITERS and delimiter not in self.UNAUTHORIZED_DELIMITERS:
                    data['CustomerAttributesDelimiter'] = delimiter
                else:
                    raise Exception('Invalid delimiter')

        response = self.client.get(self._get_url(), data)
        if not response:
            return False

        results = list()
        for item in response.json():
            result = {
                'customer_id': item['CustomerID'],
                'initial_customer_attribute': item['InitialCustomerAttribute'],
                'final_customer_attribute': item['FinalCustomerAttribute']
            }
            if attributes:
                customer_attributes = item['CustomerAttributes'].split(delimiter)
                for index, attribute in enumerate(attributes):
                    result['attributes'][attribute] = customer_attributes[index]
            results.append(result)

        return results

    def get_customer_future_values(self, life_cycle_stage_id=None, attribute=None, attribute_value=None):
        """Returns customer IDs and their current future values."""
        data = {}
        if life_cycle_stage_id:
            data['LifeCycleStageID'] = life_cycle_stage_id

        if attribute and attribute_value:
            data['CustomerAttribute'] = attribute
            data['CustomerAttributeValue'] = attribute_value

        response = self.client(self._get_url(), data) if data else self.client(self._get_url())
        if not response:
            return False

        results = {}
        for item in response.json():
            results[item['CustomerID']] = item['FutureValue']

        return results

    def get_customer_last_action_executed(self, customer_id):
        """Returns details of the last action executed for a particular customer ID."""
        if not customer:
            raise Exception('No CustomerID provided')

        data = {
            'CustomerID': customer_id
        }

        response = self.client.get(self._get_url(), data)
        if not response:
            return False

        item = response.json()
        return {
            'customer_id': customer_id,
            'action_id': item['ActionID'],
            'date': item['Date'],
            'duration': item['Duration'],
            'target_group_id': item['TargetGroupID']
        }

    def get_customer_action_details_by_date(self, date):
        """Returns customer IDs and details of the campaigns sent to them on a particular date."""
        if not date:
            raise Exception('No Date provided')

        data = {
            'Date': date
        }

        response = self.client.get(self._get_url(), data)
        if not response:
            return False

        results = list()
        for item in response.json():
            result = {
                'customer_id': item['CustomerID'],
                'recipient_group_id': item['RecipientGroupID'],
                'action_id': item['ActionID'],
                'channel_id': item['ChannelID']
            }
            results.append(result)

        return results

    def get_customers_actions_ended_by_date(self, date):
        """Returns customer IDs and details of the campaigns they received, for action durations which ended on a
        particular date."""
        if not date:
            raise Exception('No Date provided')

        data = {
            'Date': date
        }

        response = self.client.get(self._get_url(), data)
        if not response:
            return False

        results = list()
        for item in response.json():
            result = {
                'customer_id': item['CustomerID'],
                'target_group_id': item['TargetGroupID'],
                'action_id': item['ActionID'],
                'date': item['Date'],
                'duration': item['Duration'],
                'channel_id': item['ChannelID']
            }
            results.append(result)

        return results

    def get_customer_send_details_by_campaign(self, campaign_id, include_templates_ids=False):
        """Returns an array of all customer IDs, channel IDs, send times and channel send IDs for
        a particular campaign ID."""
        if not campaign_id:
            raise Exception('No CampaignID provided')

        data = {
            'CampaignID': campaign_id
        }

        if include_templates_ids:
            data['IncludeTemplateIDs'] = True

        response = self.client.get(self._get_url(), data)
        if not response:
            return False

        results = list()
        for item in response.json():
            result = {
                'customer_id': item['CustomerID'],
                'channel_id': item['CustomerID'],
                'scheduled_time': item['CustomerID'],
                'send_id': item['SendID']
            }
            if include_templates_ids:
                data['template_id'] = item['TemplateID']
            results.append(result)

        return results

    def get_customer_send_details_by_channel(self, channel_id, campaign_id, attributes=None, delimiter=';'):
        """Returns an array of all customer IDs, template IDs, send times and customer attributes for a particular
        combination of channel ID and campaign ID."""
        if not channel_id or not campaign_id:
            raise Exception('No ChannelID and CampaignID provided')

        data = {
            'ChannelID': channel_id,
            'CampaignID': campaign_id
        }

        if attributes and type(attributes) == type(list):
            attributes = ';'.join(attributes)
            data['CustomerAttributes'] = attributes

            if delimiter:
                if delimiter in self.AUTHORIZED_DELIMITERS and delimiter not in self.UNAUTHORIZED_DELIMITERS:
                    data['CustomerAttributesDelimiter'] = delimiter
                else:
                    raise Exception('Invalid delimiter')

        response = self.client.get(self._get_url(), data)
        if not response:
            return False

        results = list()
        for item in response.json():
            result = {
                'customer_id': item['CustomerID'],
                'template_id': item['TemplateID'],
                'scheduled_time': item['ScheduledTime'],
                'send_id': item['SendID']
            }
            if attributes:
                customer_attributes = item['CustomerAttributes'].split(delimiter)
                for index, attribute in enumerate(attributes):
                    result['attributes'][attribute] = customer_attributes[index]
            results.append(result)

        return results

    def get_currently_targeted_customers(self):
        """Returns an array of all customer IDs currently included in one or more campaigns."""
        response = self.client.get(self._get_url())
        if not response:
            return False

        results = list()
        for item in response.json():
            result = {
                'customer_id': item['CustomerID'],
                'campaign_id': item['CampaignID'],
                'action_id': item['ActionID'],
                'start_date': item['StartDate'],
                'end_date': item['EndDate']
            }
            results.append(result)

        return results

    def get_cancelled_campaign_customers(self, campaign_id):
        """Returns an array of all customer IDs that had been included in a campaign that was canceled, along with their
        associated action IDs and promo codes."""
        if not campaign_id:
            raise Exception('No CampaignID provided')

        response = self.client.get(self._get_url(), data)
        if not response:
            return False

        results = list()
        for item in response.json():
            result = {
                'customer_id': item['CustomerID'],
                'action_id': item['ActionID'],
                'promo_code': item['PromoCode']
            }
            results.append(result)

        return results