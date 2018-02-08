# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from constants import AUTHORIZED_DELIMITERS, UNAUTHORIZED_DELIMITERS


class Customers(object):
    client = None

    def __init__(self, client):
        self.client = client

    def get_customers_by_action(self, recipient_group_id, action_id, date, attributes=None, delimiter=';',
                                top=None, skip=None):
        """Returns the list of customer IDs associated with a particular recipient group and action on
        a particular date, plus an optional customer attribute."""
        if not recipient_group_id or not action_id or not date:
            raise Exception('No RecipientGroupID, ActionID and Date provided')

        data = {
            'RecipientGroupID': recipient_group_id,
            'ActionID': action_id,
            'Date': date
        }

        if attributes and type(attributes) == list:
            data['CustomerAttributes'] = ';'.join(attributes)

            if delimiter:
                if delimiter in AUTHORIZED_DELIMITERS and delimiter not in UNAUTHORIZED_DELIMITERS:
                    data['CustomerAttributesDelimiter'] = delimiter
                else:
                    raise Exception('Invalid delimiter')

        if top and type(top) == int:
            data['$top'] = top

        if skip and type(skip) == int:
            data['$skip'] = skip

        response = self.client.get(self.client.get_url(), data)
        if not response:
            return False

        if attributes and type(attributes) == list:
            results = list()
            for item in response.json():
                result = {
                    'customer_id': item['CustomerID'],
                    'attributes': {
                        key: value for key, value in zip(attributes, item['CustomerAttributes'])
                    }
                }
                results.append(result)

        else:
            results = [item['CustomerID'] for item in response.json()]

        return results

    def get_customer_actions_by_target_group(self, target_group_id, date,
                                             channel_id=None,
                                             include_control_group=False, include_recipient_group_id=False,
                                             attributes=None, delimiter=';',
                                             top=None, skip=None):
        """Returns a list of customers and the details of the marketing actions they received, for a
        particular target group ID on a particular date."""
        if not target_group_id or not date:
            raise Exception('No TargetGroupID and Date provided')

        data = {
            'TargetGroupID': target_group_id,
            'Date': date
        }

        if channel_id:
            data['ChannelID'] = channel_id

        if include_recipient_group_id:
            data['IncludeRecipientGroupID'] = True

        if include_control_group:
            data['IncludeControlGroup'] = True

        if attributes and type(attributes) == list:
            data['CustomerAttributes'] = ';'.join(attributes)

            if delimiter:
                if delimiter in AUTHORIZED_DELIMITERS and delimiter not in UNAUTHORIZED_DELIMITERS:
                    data['CustomerAttributesDelimiter'] = delimiter
                else:
                    raise Exception('Invalid delimiter')

        if top and type(top) == int:
            data['$top'] = top

        if skip and type(skip) == int:
            data['$skip'] = skip

        response = self.client.get(self.client.get_url(), data)
        if not response:
            return False

        results = list()
        for item in response.json():
            result = {
                'customer_id': item['CustomerID'],
                'action_id': item['ActionID'],
                'channel_id': item['ChannelID']
            }
            if attributes and type(attributes) == list:
                result['attributes'] = {
                    key: value for key, value in zip(attributes, item['CustomerAttributes'])
                }

            if include_recipient_group_id:
                result['recipient_group_id'] = item['RecipientGroupID']

            results.append(result)

        return results

    def get_customer_one_time_actions_by_date(self, date, include_control_group=False, attributes=None, delimiter=';',
                                              top=None, skip=None):
        """Returns a list of customers and the details of the marketing actions they received as part of one-time
        campaigns executed on a particular date."""
        if not date:
            raise Exception('No Date provided')

        data = {
            'Date': date
        }

        if include_control_group:
            data['IncludeControlGroup'] = True

        if attributes and type(attributes) == list:
            data['CustomerAttributes'] = ';'.join(attributes)

            if delimiter:
                if delimiter in AUTHORIZED_DELIMITERS and delimiter not in UNAUTHORIZED_DELIMITERS:
                    data['CustomerAttributesDelimiter'] = delimiter
                else:
                    raise Exception('Invalid delimiter')

        if top and type(top) == int:
            data['$top'] = top

        if skip and type(skip) == int:
            data['$skip'] = skip

        response = self.client.get(self.client.get_url(), data)
        if not response:
            return False

        results = list()
        for item in response.json():
            result = {
                'customer_id': item['CustomerID'],
                'action_id': item['ActionID'],
                'channel_id': item['ChannelID']
            }
            if attributes and type(attributes) == list:
                result['attributes'] = {
                    key: value for key, value in zip(attributes, item['CustomerAttributes'])
                }
            results.append(result)

        return results

    def get_customer_one_time_actions_by_campaign(self, campaign_id, include_control_group=False,
                                                  attributes=None, delimiter=';',
                                                  top=None, skip=None):
        """Returns a list of customers and the details associated with a particular one-time campaign."""
        if not campaign_id:
            raise Exception('No CampaignID provided')

        data = {
            'CampaignID': campaign_id
        }

        if include_control_group:
            data['IncludeControlGroup'] = True

        if attributes and type(attributes) == list:
            data['CustomerAttributes'] = ';'.join(attributes)

            if delimiter:
                if delimiter in AUTHORIZED_DELIMITERS and delimiter not in UNAUTHORIZED_DELIMITERS:
                    data['CustomerAttributesDelimiter'] = delimiter
                else:
                    raise Exception('Invalid delimiter')

        if top and type(top) == int:
            data['$top'] = top

        if skip and type(skip) == int:
            data['$skip'] = skip

        response = self.client.get(self.client.get_url(), data)
        if not response:
            return False

        results = list()
        for item in response.json():
            result = {
                'customer_id': item['CustomerID'],
                'action_id': item['ActionID'],
                'channel_id': item['ChannelID']
            }
            if attributes and type(attributes) == list:
                result['attributes'] = {
                    key: value for key, value in zip(attributes, item['CustomerAttributes'])
                }
            results.append(result)

        return results

    def get_target_group_changers(self, start_date, end_date, attributes=None, delimiter=';', top=None, skip=None):
        """Returns the before and after target group IDs for customers whose target group changed during a particular
        date range."""
        if not start_date or not end_date:
            raise Exception('No StartDate and EndDate provided')

        data = {
            'StartDate': start_date,
            'EndDate': end_date
        }

        if attributes and type(attributes) == list:
            data['CustomerAttributes'] = ';'.join(attributes)

            if delimiter:
                if delimiter in AUTHORIZED_DELIMITERS and delimiter not in UNAUTHORIZED_DELIMITERS:
                    data['CustomerAttributesDelimiter'] = delimiter
                else:
                    raise Exception('Invalid delimiter')

        if top and type(top) == int:
            data['$top'] = top

        if skip and type(skip) == int:
            data['$skip'] = skip

        response = self.client.get(self.client.get_url(), data)
        if not response:
            return False

        results = list()
        for item in response.json():
            result = {
                'customer_id': item['CustomerID'],
                'initial_target_group_id': item['InitialTargetGroupID'],
                'final_target_group_id': item['FinalTargetGroupID']
            }
            if attributes and type(attributes) == list:
                result['attributes'] = {
                    key: value for key, value in zip(attributes, item['CustomerAttributes'])
                }
            results.append(result)

        return results

    def get_customer_attribute_changers(self, start_date, end_date, changed_customer_attribute,
                                        attributes=None, delimiter=';', top=None, skip=None):
        """Returns an array of customer IDs, and their before and after attribute values, for customers whose selected
        attribute changed during a particular date range."""
        if not start_date or not end_date or not changed_customer_attribute:
            raise Exception('No StartDate, EndDate and ChangedCustomerAttribute provided')

        data = {
            'StartDate': start_date,
            'EndDate': end_date,
            'ChangedCustomerAttribute': changed_customer_attribute
        }

        if attributes and type(attributes) == list:
            data['CustomerAttributes'] = ';'.join(attributes)

            if delimiter:
                if delimiter in AUTHORIZED_DELIMITERS and delimiter not in UNAUTHORIZED_DELIMITERS:
                    data['CustomerAttributesDelimiter'] = delimiter
                else:
                    raise Exception('Invalid delimiter')

        if top and type(top) == int:
            data['$top'] = top

        if skip and type(skip) == int:
            data['$skip'] = skip

        response = self.client.get(self.client.get_url(), data)
        if not response:
            return False

        results = list()
        for item in response.json():
            result = {
                'customer_id': item['CustomerID'],
                'initial_customer_attribute': None if item['InitialCustomerAttribute'] == 'NULL'
                else item['InitialCustomerAttribute'],
                'final_customer_attribute': None if item['FinalCustomerAttribute'] == 'NULL'
                else item['FinalCustomerAttribute']
            }
            if attributes and type(attributes) == list:
                result['attributes'] = {
                    key: value for key, value in zip(attributes, item['CustomerAttributes'])
                }
            results.append(result)

        return results

    def get_customer_future_values(self, life_cycle_stage_id=None, attribute=None, attribute_value=None,
                                   top=None, skip=None):
        """Returns customer IDs and their current future values."""
        if not life_cycle_stage_id and not attribute and not attribute_value:
            raise Exception('No LifecycleStageID or CustomerAttribute and CustomerAttributeValue provided')

        if life_cycle_stage_id and not attribute and not attribute_value:
            data = {'LifecycleStageID': life_cycle_stage_id}

        elif not life_cycle_stage_id and attribute and attribute_value:
            data = {
                'CustomerAttribute': attribute,
                'CustomerAttributeValue': attribute_value
            }

        else:
            raise Exception('Wrong combination for LifecycleStageID, CustomerAttribute and CustomerAttributeValue')

        if top and type(top) == int:
            data['$top'] = top

        if skip and type(skip) == int:
            data['$skip'] = skip

        response = self.client.get(self.client.get_url(), data)
        if not response:
            return False

        results = {}
        for item in response.json():
            results[item['CustomerID']] = item['FutureValue']

        return results

    def get_customer_last_action_executed(self, customer_id):
        """Returns details of the last action executed for a particular customer ID."""
        if not customer_id:
            raise Exception('No CustomerID provided')

        data = {
            'CustomerID': customer_id
        }

        response = self.client.get(self.client.get_url(), data)
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

    def get_customer_action_details_by_date(self, date, top=None, skip=None):
        """Returns customer IDs and details of the campaigns sent to them on a particular date."""
        if not date:
            raise Exception('No Date provided')

        data = {
            'Date': date
        }

        if top and type(top) == int:
            data['$top'] = top

        if skip and type(skip) == int:
            data['$skip'] = skip

        response = self.client.get(self.client.get_url(), data)
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

    def get_customers_action_ended_by_date(self, date, top=None, skip=None):
        """Returns customer IDs and details of the campaigns they received, for action durations which ended on a
        particular date."""
        if not date:
            raise Exception('No Date provided')

        data = {
            'Date': date
        }

        if top and type(top) == int:
            data['$top'] = top

        if skip and type(skip) == int:
            data['$skip'] = skip

        response = self.client.get(self.client.get_url(), data)
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

    def get_customer_send_details_by_campaign(self, campaign_id, include_templates_ids=False, top=None, skip=None):
        """Returns an array of all customer IDs, channel IDs, send times and channel send IDs for
        a particular campaign ID."""
        if not campaign_id:
            raise Exception('No CampaignID provided')

        data = {
            'CampaignID': campaign_id
        }

        if include_templates_ids:
            data['IncludeTemplateIDs'] = True

        if top and type(top) == int:
            data['$top'] = top

        if skip and type(skip) == int:
            data['$skip'] = skip

        response = self.client.get(self.client.get_url(), data)
        if not response:
            return False

        results = list()
        for item in response.json():
            result = {
                'customer_id': item['CustomerID'],
                'channel_id': item['ChannelID'],
                'scheduled_time': item['ScheduledTime'],
                'send_id': item['SendID']
            }
            if include_templates_ids:
                result['template_id'] = item['TemplateID']
            results.append(result)

        return results

    def get_customer_send_details_by_channel(self, channel_id, campaign_id, attributes=None, delimiter=';',
                                             top=None, skip=None):
        """Returns an array of all customer IDs, template IDs, send times and customer attributes for a particular
        combination of channel ID and campaign ID."""
        if not channel_id or not campaign_id:
            raise Exception('No ChannelID and CampaignID provided')

        data = {
            'ChannelID': channel_id,
            'CampaignID': campaign_id
        }

        if attributes and type(attributes) == list:
            data['CustomerAttributes'] = ';'.join(attributes)

            if delimiter:
                if delimiter in AUTHORIZED_DELIMITERS and delimiter not in UNAUTHORIZED_DELIMITERS:
                    data['CustomerAttributesDelimiter'] = delimiter
                else:
                    raise Exception('Invalid delimiter')

        if top and type(top) == int:
            data['$top'] = top

        if skip and type(skip) == int:
            data['$skip'] = skip

        response = self.client.get(self.client.get_url(), data)
        if not response:
            return False

        results = list()
        for item in response.json():
            result = {
                'customer_id': item['CustomerID'],
                'template_id': item['TemplateID'],
                'scheduled_time': item['ScheduledTime']
            }
            if attributes and type(attributes) == list:
                result['attributes'] = {
                    key: value for key, value in zip(attributes, item['CustomerAttributes'])
                }
            results.append(result)

        return results

    def get_currently_targeted_customers(self, top=None, skip=None):
        """Returns an array of all customer IDs currently included in one or more campaigns."""

        data = {}
        if top and type(top) == int:
            data['$top'] = top

        if skip and type(skip) == int:
            data['$skip'] = skip

        response = self.client.get(self.client.get_url()) if not data else self.client.get(self.client.get_url(), data)

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

    def get_canceled_campaign_customers(self, campaign_id, top=None, skip=None):
        """Returns an array of all customer IDs that had been included in a campaign that was canceled, along with their
        associated action IDs and promo codes."""
        if not campaign_id:
            raise Exception('No CampaignID provided')

        data = {'CampaignID': campaign_id}

        if top and type(top) == int:
            data['$top'] = top

        if skip and type(skip) == int:
            data['$skip'] = skip

        response = self.client.get(self.client.get_url(), data)
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
