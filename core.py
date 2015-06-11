class Core:
    def __init__(self):
        self.data = {}
        self.data_for_display = {}
        self.current_index = 0
        self.current_index_for_display = -1
        self.total_value = 0
        self.total_credit = 0
        self.result = 0

    def calculate(self):
        """
        Calculate the GPA
        :return:
        """
        for val in self.data.values():
            grade = float(val[1])
            credit = float(val[2])
            self.total_value += grade * credit
            self.total_credit += credit
        self.result = self.total_value / self.total_credit

    def reset(self):
        """
        Reset the core
        :return:
        """
        self.data = {}
        self.data_for_display = {}
        self.current_index = 0
        self.current_index_for_display = -1
        self.total_value = 0
        self.total_credit = 0
        self.result = 0

    def get_result(self):
        return self.result

    def get_total_credits(self):
        return self.total_credit

    def take_data(self, val):
        """
        Store data in form (subject, grade, credits)
        :param val:
        :return:
        """
        self.data[self.current_index] = val
        self.current_index += 1
        if self.current_index_for_display == 8:
            self.current_index_for_display = 0
            self.data_for_display[self.current_index_for_display] = val
        else:
            self.current_index_for_display += 1
            self.data_for_display[self.current_index_for_display] = val

    def get_data_display(self):
        return self.data_for_display

    def get_data(self):
        return self.data


