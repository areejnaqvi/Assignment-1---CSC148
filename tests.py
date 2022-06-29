import course
import survey
import criterion
import grouper
import pytest
import example_usage
from typing import List, Set, FrozenSet

AREEJ = course.Student(10, 'Areej')
ALYZEH = course.Student(12, 'Alyzeh')
ZAIN = course.Student(1, 'Zain')
HUSSAIN = course.Student(5, 'Hussain')
SUKAINA = course.Student(3, 'Sukaina')
MCQ = survey.MultipleChoiceQuestion(1, 'What is your gender?', ['Male', 'Female',
                                    'Other', 'Prefer not to say'])
NQ = survey.NumericQuestion(2, 'How old are you?', 16, 69)
YNQ = survey.YesNoQuestion(3, 'Do you have siblings?')
CQ = survey.CheckboxQuestion(4, 'Where do you study?', ['School', 'College',
                                                        'University', 'Other'])


def create_students() -> List[course.Student]:
    """Create a list of 5 students, completely initialised with answers
    as well"""

    AREEJ.set_answer(MCQ, survey.Answer('Female'))
    AREEJ.set_answer(NQ, survey.Answer(20))
    AREEJ.set_answer(YNQ, survey.Answer(True))
    AREEJ.set_answer(CQ, survey.Answer(['University']))

    ALYZEH.set_answer(MCQ, survey.Answer('Female'))
    ALYZEH.set_answer(NQ, survey.Answer(18))
    ALYZEH.set_answer(YNQ, survey.Answer(True))
    ALYZEH.set_answer(CQ, survey.Answer(['College']))

    ZAIN.set_answer(MCQ, survey.Answer('Male'))
    ZAIN.set_answer(NQ, survey.Answer(17))
    ZAIN.set_answer(YNQ, survey.Answer(True))
    ZAIN.set_answer(CQ, survey.Answer(['School']))

    HUSSAIN.set_answer(MCQ, survey.Answer('Male'))
    HUSSAIN.set_answer(NQ, survey.Answer(16))
    HUSSAIN.set_answer(YNQ, survey.Answer(True))
    HUSSAIN.set_answer(CQ, survey.Answer(['School']))

    SUKAINA.set_answer(MCQ, survey.Answer('Female'))
    SUKAINA.set_answer(NQ, survey.Answer(16))
    SUKAINA.set_answer(YNQ, survey.Answer(True))
    SUKAINA.set_answer(CQ, survey.Answer(['School']))

    students = [AREEJ, ALYZEH, ZAIN, HUSSAIN, SUKAINA]
    return students


def create_course() -> course.Course:
    """Create a course full of 5 students"""
    c = course.Course('CSC148')
    students = create_students()
    c.enroll_students([students])
    return c


def create_survey() -> survey.Survey:
    """Create a fully initialised survey"""
    basic_info = survey.Survey([MCQ, NQ, YNQ, CQ])
    basic_info.set_weight(2, MCQ)
    basic_info.set_weight(3, NQ)
    basic_info.set_weight(1, YNQ)
    basic_info.set_weight(4, CQ)
    return basic_info

# TESTS FOR SLICE_LIST


def test_slice_list_larger() -> None:
    """Test slice_list where the size of the sliced list is less than the
    length of the list"""
    sliced = grouper.slice_list([1, 2, 3, 4, 5, 6, 7, 8, 9], 2)
    assert sliced == [[1, 2], [3, 4], [5, 6], [7, 8], [9]]


def test_slice_list_equal() -> None:
    """Test slice_list where n equals the length of the list"""
    sliced = grouper.slice_list([1, 2, 3, 4, 5], 5)
    assert sliced == [[1, 2, 3, 4, 5]]


def test_slice_list_empty() -> None:
    """Test slice_list on an empty list"""
    sliced = grouper.slice_list([], 0)
    assert sliced == []


def test_slice_list_zero() -> None:
    """Test slice_list when n = 0"""
    sliced = grouper.slice_list([1, 2, 3, 4, 5, 6, 7, 8, 9], 0)
    assert sliced == []


def test_slice_list_negative_n() -> None:
    """Test slice_list when n < 0"""
    sliced = grouper.slice_list([1, 2, 3, 4, 5], -1)
    assert sliced == []


# TESTS FOR WINDOWS


def test_windows_larger() -> None:
    """Test windows where the size of the sliced list is larger than the
    length of the list"""
    window = grouper.windows([1, 2, 3, 4, 5, 6, 7, 8, 9], 5)
    assert window == [[1, 2, 3, 4, 5], [2, 3, 4, 5, 6], [3, 4, 5, 6, 7],
                      [4, 5, 6, 7, 8], [5, 6, 7, 8, 9]]


def test_windows_equal() -> None:
    """Test windows when n equals the length of the list"""
    window = grouper.windows([1, 2, 3, 4, 5], 5)
    assert window == [[1, 2, 3, 4, 5]]


def test_windows_empty() -> None:
    """Test windows when the input list is empty"""
    window = grouper.windows([], 0)
    assert window == []


def test_windows_zero() -> None:
    """Test windows when n=0"""
    window = grouper.windows([1, 2, 3, 4, 5], 0)
    assert window == []


def test_windows_negative_n() -> None:
    """Test windows when n < 0"""
    window = grouper.windows([1, 2, 3, 4, 5], -5)
    assert window == []

# TESTS FOR _MAX_SCORE


def test_max_score_areej() -> None:
    """Test _max_score to ensure that it outputs the correct index to form the
    highest scoring group with AREEJ."""
    students = create_students()
    students.remove(AREEJ)
    s = create_survey()
    i = grouper._max_score(AREEJ, s, students)
    assert i == 0


def test_max_score_alyzeh() -> None:
    """Test _max_score to ensure that it outputs the correct index to form the
    highest scoring group with ALYZEH."""
    students = create_students()
    students.remove(ALYZEH)
    s = create_survey()
    i = grouper._max_score(ALYZEH, s, students)
    assert i == 0

# TESTS FOR AlphaGrouper


def test_alpha_grouper_make_grouping_reg() -> None:
    """Test make_grouping with a survey of 4 questions and a course with
    5 enrolled students, all of whom contain valid answers to all questions in
    the survey"""
    course = create_course()
    survey = create_survey()
    alpha_grouper = grouper.AlphaGrouper(2)
    alpha_grouper.make_grouping(course, survey)
    mine = grouper.Grouping()
    group1 = grouper.Group([ALYZEH, AREEJ])
    group2 = grouper.Group([HUSSAIN, SUKAINA])
    group3 = grouper.Group([ZAIN])
    mine.add_group(group1)
    mine.add_group(group2)
    mine.add_group(group3)

    assert mine._groups == alpha_grouper._groups


def test_alpha_grouper_make_grouping_empty() -> None:
    """Test make_grouping with a survey of 4 questions and a course with
     no enrolled students."""
    c = course.Course('csc148')
    survey = create_survey()
    alpha_grouper = grouper.AlphaGrouper(2)
    ag = alpha_grouper.make_grouping(c, survey)
    mine = grouper.Grouping()
    assert mine._groups == ag._groups


def test_alpha_grouper_make_grouping_same_name_diff_ids() -> None:
    """Test make_grouping with a survey of 4 questions and a course with
    5 enrolled students."""
    sukaina = course.Student(3, 'Areej')
    c = course.Course('CSC148')
    c.enroll_students([AREEJ, ALYZEH, ZAIN, HUSSAIN,
                       sukaina])
    survey = create_survey()
    alpha_grouper = grouper.AlphaGrouper(2)
    ag = alpha_grouper.make_grouping(course, survey)
    mine = grouper.Grouping()
    group1 = grouper.Group([ALYZEH, AREEJ])
    group2 = grouper.Group([sukaina, HUSSAIN])
    group3 = grouper.Group([ZAIN])
    mine.add_group(group1)
    mine.add_group(group2)
    mine.add_group(group3)
    assert mine._groups == ag._groups


def test_alpha_grouper_make_grouping_smaller_group_size() -> None:
    """Test make_grouping with a survey of 4 questions and a course with
    5 enrolled student. The group size for the grouping will be larger than 5"""
    course = create_course()
    survey = create_survey()
    alpha_grouper = grouper.AlphaGrouper(6)
    ag = alpha_grouper.make_grouping(course, survey)
    mine = grouper.Grouping()
    group1 = grouper.Group([ALYZEH, AREEJ, HUSSAIN, SUKAINA, ZAIN])
    mine.add_group(group1)
    assert mine._groups == ag._groups


def test_alpha_grouper_make_grouping_equal_group_size() -> None:
    """Test make_grouping with a survey of 4 questions and a course with
     5 enrolled students. The group size for the group equals 5."""
    course = create_course()
    survey = create_survey()
    alpha_grouper = grouper.AlphaGrouper(5)
    ag = alpha_grouper.make_grouping(course, survey)
    mine = grouper.Grouping()
    group1 = grouper.Group([ALYZEH, AREEJ, HUSSAIN, SUKAINA, ZAIN])
    mine.add_group(group1)
    assert mine._groups == ag._groups

# TEST RANDOM GROUPER


def test_random_grouper_make_grouping_length() -> None:
    """Test make_grouping with a survey of 4 questions and a course with
    5 enrolled students."""
    c = create_course()
    s = create_survey()
    random_grouper = grouper.RandomGrouper(2)
    rg = random_grouper.make_grouping(c, s)
    mine = grouper.Grouping()
    group1 = grouper.Group([ALYZEH, AREEJ])
    group2 = grouper.Group([HUSSAIN, SUKAINA])
    group3 = grouper.Group([ZAIN])
    mine.add_group(group1)
    mine.add_group(group2)
    mine.add_group(group3)
    assert len(mine.get_groups()) == len(rg.get_groups())

# TEST GREEDY GROUPER


def test_greedy_grouper_make_grouping_reg() -> None:
    """Test make_grouping with a survey of 4 questions and a course with
    5 enrolled students."""
    score = example_usage.make_grouping_float()
    assert score == 1.0416666666666667

# TEST WINDOW GROUPER


def test_window_grouper_make_grouping() -> None:
    """"Test make_grouping with a survey of 4 questions and a course with
    5 enrolled students."""
    score = example_usage.make_grouping_float()
    assert score == 1.0416666666666667

# TEST GROUP


def test_group_empty_length() -> None:
    """Test the __len__ method with an empty group"""
    group = grouper.Group([])
    assert len(group) == 0


def test_group_length_reg() -> None:
    """Test the __len__ method with a regular group"""
    group = grouper.Group([AREEJ, ALYZEH, HUSSAIN, SUKAINA, ZAIN])
    assert len(group) == 5


def test_contains_present() -> None:
    """Test the __contains__ method where the Student is present in
    the group"""
    group = grouper.Group([ALYZEH, AREEJ, HUSSAIN, SUKAINA, ZAIN])
    assert SUKAINA in group


def test_contains_present_same_name() -> None:
    """Test the __contains__ method where the student is not present
    in the group but someone else with the same name is."""
    group = grouper.Group([ALYZEH, AREEJ, HUSSAIN, SUKAINA, ZAIN])
    areej = course.Student(1005452350, 'Areej')
    assert areej not in group


def test_contains_not_present() -> None:
    """Test the __contains__ method where the student is not present
    in the group"""
    group = grouper.Group([ALYZEH, AREEJ, HUSSAIN, SUKAINA, ZAIN])
    sakina = course.Student(25, 'Sakina')
    assert sakina not in group


def test_str_representation() -> None:
    """Test whether the string comes out the way its supposed to"""
    group = grouper.Group([ALYZEH, AREEJ, HUSSAIN, SUKAINA, ZAIN])
    names = 'Alyzeh, Areej, Hussain, Sukaina, Zain.'
    assert str(group) == names


def test_str_representation_empty() -> None:
    """Test whether the string correctly returns an empty string for an
    empty group"""
    group = grouper.Group([])
    assert str(group) == ''


def test_get_members() -> None:
    """Test to ensure that the inputted list isnt mutated by the method"""
    students = create_students()
    group = grouper.Group(students)
    new = group.get_members()
    assert new == students
    assert students == [AREEJ, ALYZEH, ZAIN, HUSSAIN, SUKAINA]

# TEST GROUPING


def test_grouping_empty_list() -> None:
    """Test __len__ for empty list"""
    g = grouper.Grouping()
    assert len(g) == 0


def test_grouping_regular_grouping() -> None:
    """Test __len__ for a regularly initialised grouping"""
    grouping = grouper.Grouping()
    group1 = grouper.Group([ALYZEH, AREEJ])
    group2 = grouper.Group([HUSSAIN, SUKAINA])
    group3 = grouper.Group([ZAIN])
    grouping.add_group(group1)
    grouping.add_group(group2)
    grouping.add_group(group3)
    assert len(grouping) == 3


def test_grouping_str_empty() -> None:
    """Test __str__ for an empty grouping."""
    grouping = grouper.Grouping()
    assert str(grouping) == ''


def test_grouping_str_non_empty() -> None:
    """Test __str__ for a non-empty grouping."""
    grouping = grouper.Grouping()
    group1 = grouper.Group([ALYZEH, AREEJ])
    group2 = grouper.Group([HUSSAIN, SUKAINA])
    group3 = grouper.Group([ZAIN])
    grouping.add_group(group1)
    grouping.add_group(group2)
    grouping.add_group(group3)
    name = 'Alyzeh, Areej.\nHussain, Sukaina.\nZain.\n'
    assert name == str(grouping)


def test_grouping_add_group() -> None:
    """Test add_group when a student in the group is already in a group
    in the grouping"""
    grouping = grouper.Grouping()
    group1 = grouper.Group([ALYZEH, AREEJ])
    group2 = grouper.Group([HUSSAIN, SUKAINA])
    group3 = grouper.Group([ALYZEH, ZAIN])
    grouping.add_group(group1)
    grouping.add_group(group2)
    grouping.add_group(group3)
    assert len(grouping) == 2
    for f in grouping._groups:
        not_added = group3 != f
    assert not_added


def test_grouping_add_group_valid_entry() -> None:
    """Test add_group when the group to be added does not have any
    students that are already present in groups in the grouping."""
    grouping = grouper.Grouping()
    group1 = grouper.Group([ALYZEH, AREEJ])
    group2 = grouper.Group([HUSSAIN, SUKAINA])
    group3 = grouper.Group([ZAIN])
    grouping.add_group(group1)
    grouping.add_group(group2)
    grouping.add_group(group3)
    g1 = g2 = g3 = False
    g4 = True
    for g in grouping._groups:
        if group1 == g:
            g1 = True
        elif group2 == g:
            g2 = True
        elif group3 == g:
            g3 = True
        else:
            g4 = False
    assert g1 and g2 and g3 and g4


def test_grouping_add_group_empty_addition() -> None:
    """Test add_group when the group to be added is empty."""
    grouping = grouper.Grouping()
    group1 = grouper.Group([ALYZEH, AREEJ])
    group2 = grouper.Group([HUSSAIN, SUKAINA])
    group3 = grouper.Group([])
    grouping.add_group(group1)
    grouping.add_group(group2)
    grouping.add_group(group3)
    g1 = g2 = g3 = False
    g4 = True
    for g in grouping._groups:
        if group1 == g:
            g1 = True
        elif group2 == g:
            g2 = True
        elif group3 == g:
            g3 = True
        else:
            g4 = True
    assert g1 and g2 and (not g3) and g4


def test_grouping_get_groups() -> None:
    """Test get_groups for mutation and correct returning value"""
    grouping = grouper.Grouping()
    group1 = grouper.Group([ALYZEH, AREEJ])
    group2 = grouper.Group([HUSSAIN, SUKAINA])
    group3 = grouper.Group([ZAIN])
    grouping.add_group(group1)
    grouping.add_group(group2)
    grouping.add_group(group3)
    shallow_groups = grouping.get_groups()
    assert shallow_groups == [group1, group2, group3]
    shallow_groups.append(1)
    assert shallow_groups != grouping._groups

# TEST MCQ SUBCLASS OF QUESTION


def test_mcq_str_regular() -> None:
    """Test __str__ for MultipleChoiceQuestion"""
    req = 'Q. What is your gender?\n\nMale\nFemale\nOther\nPrefer not to say\n'
    assert req == str(MCQ)


def test_mcq_validate_answer() -> None:
    """Test validate_answer for MCQ"""
    valid = MCQ.validate_answer(survey.Answer('Female'))
    assert valid


def test_mcq_validate_answer_not_str() -> None:
    """Test validate_answer for MCQ when answer.content is not a string"""
    valid = MCQ.validate_answer(survey.Answer(['A']))
    assert not valid


def test_mcq_validate_answer_not_option() -> None:
    """Test validate_answer for MCQ when answer.content is not in
    self.options"""
    valid = MCQ.validate_answer(survey.Answer('a'))
    assert not valid


def test_mcq_validate_answer_case_sensitivity() -> None:
    """Test validate_answer for no case sensitivity"""
    valid = MCQ.validate_answer(survey.Answer('FEMALE'))
    assert not valid


def test_mcq_get_similarity_1() -> None:
    """Test get_similiarity for MCQ"""
    f = MCQ.get_similarity(survey.Answer('Female'), survey.Answer('Female'))
    assert f == 1.0


def test_mcq_get_similarity_case_sensitivity() -> None:
    """Test get_similarity for lack of case sensitivity"""
    f = MCQ.get_similarity(survey.Answer('FEMALE'), survey.Answer('female'))
    assert f == 0.0


def test_mcq_get_similarity_0() -> None:
    """Test get_similarity for MCQ (non similar)"""
    f = MCQ.get_similarity(survey.Answer('Female'), survey.Answer('Male'))
    assert f == 0.0

# TEST NUMERICQUESTION (SUBCLASS OF QUESTION)


def test_nq_str() -> None:
    """Test string representation for numeric questions"""
    req = 'Q. How old are you?\n\nYour answer must be an integer between '
    req += '16 and 69 inclusive\n'
    assert req == str(NQ)


def test_nq_validate_answer() -> None:
    """Test validate_answer for numeric question when answer.content is an
    int within range"""
    valid = NQ.validate_answer(survey.Answer(20))
    assert valid


def test_nq_validate_answer_less_than() -> None:
    """Test validate_answer for numeric questions when answer.content is
    less than the minimum"""
    valid = NQ.validate_answer(survey.Answer(10))
    assert not valid


def test_nq_validate_answer_equal_min() -> None:
    """Test validate_answer for numeric questions when answer.content is
    equal to the minimum"""
    valid = NQ.validate_answer(survey.Answer(16))
    assert valid


def test_nq_validate_answer_equal_max() -> None:
    """Test validate_answer for numeric questions when answer.content is
    equal to the maximum"""
    valid = NQ.validate_answer(survey.Answer(69))
    assert valid


def test_nq_validate_answer_greater_than() -> None:
    """Test validate_answer for numeric questions when answer.content is
    more than the maximum"""
    valid = NQ.validate_answer(survey.Answer(70))
    assert not valid


def test_nq_validate_answer_float() -> None:
    """Test validate_answer for numeric questions when answer.content is
    a float"""
    valid = NQ.validate_answer(survey.Answer(20.0))
    assert not valid


def test_get_similarity_equal() -> None:
    """Test get_similarity for numeric questions."""
    eq = NQ.get_similarity(survey.Answer(20), survey.Answer(20))
    assert eq == 1.0


def test_get_similarity_equal_max_min() -> None:
    """Test get_similarity for numeric questions when answer1 == min_
    and answer2 == max_"""
    eq = NQ.get_similarity(survey.Answer(16), survey.Answer(69))
    assert eq == 0.0


def test_get_similarity_absolute() -> None:
    """Test get_similarity for numeric questions and ensure step 1 is
    working correctly"""
    eq = NQ.get_similarity(survey.Answer(69), survey.Answer(16))
    assert eq == 0.0


def test_get_similarity_random() -> None:
    """Test get_similarity for a random input"""
    eq = NQ.get_similarity(survey.Answer(16), survey.Answer(42))
    assert eq == 0.5094339622641509

# TEST YESNOQUESTION (SUCLASS OF MCQ)


def test_ynq_str() -> None:
    """Test __str__ for YesNoQuestion"""
    req = 'Q. Do you have siblings?\n\nYour answer can only be True or False.\n'
    assert req == str(YNQ)


def test_ynq_validate_answer_true() -> None:
    """Test validate_answer for YesNoQuestion where answer.content is True"""
    valid = YNQ.validate_answer(survey.Answer(True))
    assert valid


def test_ynq_validate_answer_false() -> None:
    """Test validate_answer for YesNoQuestion where answer.content is False"""
    valid = YNQ.validate_answer(survey.Answer(False))
    assert valid is True


def test_ynq_validate_answer_not_bool() -> None:
    """Test validate_answer for YesNoQuestion where answer.content is not
    a boolean"""
    valid = YNQ.validate_answer(survey.Answer('a'))
    assert valid is False


def test_ynq_validate_answer_true_empty_list() -> None:
    """Test validate_answer for YesNoQuestion where answer.content is True"""
    valid = YNQ.validate_answer(survey.Answer([]))
    assert valid is False


def test_ynq_get_similarity_1_true() -> None:
    """Test get_similiarity for MCQ for True values"""
    f = YNQ.get_similarity(survey.Answer(True), survey.Answer(True))
    assert f == 1.0


def test_ynq_get_similarity_0() -> None:
    """Test get_similarity for MCQ (non similar)"""
    f = YNQ.get_similarity(survey.Answer(True), survey.Answer(False))
    assert f == 0.0


def test_ynq_get_similarity_1_false() -> None:
    """Test get_similarity for MCQ for False values"""
    f = YNQ.get_similarity(survey.Answer(False), survey.Answer(False))
    assert f == 1.0

# TESTS FOR CHECKBOX QUESTIONS


def test_cbq_str() -> None:
    """Test __str__ for CheckboxQuestion"""
    req = req = 'Q. Where do you study?\n\nSchool\nCollege\nUniversity\nOther\n'
    assert req == str(CQ)


def test_cbq_validate_answer_true() -> None:
    """Test validate_answer for CheckBoxQuestion"""
    valid = CQ.validate_answer(survey.Answer(['School', 'College']))
    assert valid is True


def test_cbq_validate_answer_false() -> None:
    """Test validate_answer for CheckBoxQuestion"""
    valid = CQ.validate_answer(survey.Answer(['School', 'No']))
    assert valid is False


def test_cbq_validate_answer_empty() -> None:
    """Test validate_answer for CheckBoxQuestion for empty list"""
    valid = CQ.validate_answer(survey.Answer([]))
    assert valid is False


def test_cbq_validate_answer() -> None:
    """Test validate_answer for a non unique list"""
    valid = CQ.validate_answer(survey.Answer(['School', 'College', 'University',
                                              'University']))
    assert valid is False


def test_cbq_validate_answer() -> None:
    """Test validate_answer for a non list type answer"""
    valid = CQ.validate_answer(survey.Answer([1]))
    assert not valid


def test_cbq_get_similarity_equal() -> None:
    """Test get_similarity for same answers"""
    valid = CQ.get_similarity(survey.Answer([1, 2, 3, 4, 5]),
                              survey.Answer([1, 2, 3, 4, 5]))
    assert valid == 1.0


def test_cbq_get_similarity_no_common() -> None:
    """Test get_similarity for no common answers between answers"""
    valid = CQ.get_similarity(survey.Answer([1, 2, 3]), survey.Answer([4, 5, 6])
                              )
    assert valid == 0.0


def test_cbq_get_similarity_random() -> None:
    """Test get_similarity for a random ensemble of unique and common
    elements"""
    eq = CQ.get_similarity(survey.Answer([1, 2, 3, 4]),
                           survey.Answer([2, 3, 4, 5]))
    assert eq == 0.6

# TEST ANSWER


def test_ans_is_valid_mcq() -> None:
    """Test is_valid for MultipleChoiceQuestion"""
    ans = survey.Answer('Female')
    valid = ans.is_valid(MCQ)
    assert valid


def test_ans_is_valid_nq() -> None:
    """Test is_valid for NumericQuestion"""
    ans = survey.Answer(20)
    valid = ans.is_valid(NQ)
    assert valid


def test_ans_is_valid_ynq() -> None:
    """Test is_valid for YesNoQuestion"""
    ans = survey.Answer(True)
    valid = ans.is_valid(YNQ)


def test_ans_is_valid_cbq() -> None:
    """Test is_valid for CheckboxQuestion"""
    ans = survey.Answer(['School', 'College'])
    valid = ans.is_valid(CQ)
    assert valid

# TEST SURVEY


def test_survey_length_empty() -> None:
    """Test __len__  on an empty survey with no questions"""
    s = survey.Survey([])
    assert len(s) == 0


def test_survey_length_nonempty() -> None:
    """Test __len__ on a non empty survey"""
    survey = create_survey()
    assert len(survey) == 4


def test_survey_contains_present() -> None:
    """Test __contains__ when the question is present"""
    survey = create_survey()
    valid = MCQ in survey
    assert valid


def test_survey_contains_not_present() -> None:
    """Test __contains__ when the question is not present in the survey"""
    s = survey.Survey([])
    valid = YNQ in s
    assert not valid


def test_survey_str_rep_nonempty() -> None:
    """Test __str__ on a nonempty survey"""
    s = create_survey()
    req = 'The questions in this survey are as follows: \n\nID - 1: ' + str(MCQ)
    req += '\nID - 2: ' + str(NQ) + '\nID - 3: ' + str(YNQ) + '\nID - 4: ' + \
           str(CQ) + '\n'
    assert str(s) == req


def test_survey_str_rep_empty() -> None:
    """Test __str__ on an empty survey"""
    s = survey.Survey([])
    req = 'The questions in this survey are as follows: \n\n'
    assert req == str(s)


def test_survey_get_questions_nonempty() -> None:
    """Test get_questions on a non empty list"""
    survey = create_survey()
    a = survey.get_questions()
    assert a == [MCQ, NQ, YNQ, CQ]


def test_survey_get_question_empty() -> None:
    """Test get_questions on an empty survey"""
    s = survey.Survey([])
    a = s.get_questions()
    assert a == []


def test_get_criterion_not_present() -> None:
    """Test _get_criterion where question is not present in self._criteria"""
    s = create_survey()
    a = s._get_criterion(MCQ)
    assert a == s._default_criterion


def test_get_criterion_present() -> None:
    """Test _get_criterion where question is present in self._criteria"""
    s = create_survey()
    s.set_criterion(criterion.HeterogeneousCriterion(), MCQ)
    a = s._get_criterion(MCQ)
    assert a == s._criteria[MCQ.id]


def test_get_weight_not_present() -> None:
    """Test _get_weight where question is not present in self._weights"""
    survey = create_survey()
    a = survey._get_weight(MCQ)
    assert a == 2


def test_get_weight_present() -> None:
    """Test _get_weight where question is present in self._weights"""
    survey = create_survey()
    survey.set_weight(2, MCQ)
    a = survey._get_weight(MCQ)
    assert a == 2


def test_set_weight_not_present() -> None:
    """Test set_weight when question.id is not present in self._questions"""
    s = survey.Survey([])
    valid = s.set_weight(2, MCQ)
    assert not valid
    assert s._weights == {}


def test_set_weight_present() -> None:
    """Test set_weight when question.id is present in self._questions"""
    survey = create_survey()
    valid = survey.set_weight(2, MCQ)
    assert survey._weights == {1: 2, 2: 3, 3: 1, 4: 4}
    assert valid


def test_set_criterion_not_present() -> None:
    """Test set_criterion when question.id is not present in self._questions"""
    s = survey.Survey([])
    valid = s.set_weight(criterion.HeterogeneousCriterion(), MCQ)
    assert not valid
    assert s._criteria == {}


def test_set_criterion_present() -> None:
    """Test set_weight when question.id is present in self._questions"""
    survey = create_survey()
    c = criterion.HeterogeneousCriterion()
    valid = survey.set_criterion(c, MCQ)
    assert survey._criteria == {1: c}
    assert valid


def test_score_students_homogenous() -> None:
    """Test score_students for a survey with 4 questions and a list of
    5 students."""
    s = create_survey()
    students = create_students()
    f = s.score_students(students)
    assert f == 1.4716981132075473


def test_score_students_heterogenous() -> None:
    """Test score_students for a survey with 4 questions and a list of
    5 students. The criteria is heterogenous"""
    s = create_survey()
    s._default_criterion = criterion.HeterogeneousCriterion()
    students = create_students()
    f = s.score_students(students)
    assert f == 1.0283018867924527


def test_score_grouping_homogenous() -> None:
    """Test score_grouping for a survey with 4 questions and a grouping
    with 3 groups (total 5 students)"""
    g = grouper.Grouping()
    g1 = grouper.Group([AREEJ, ALYZEH])
    g2 = grouper.Group([SUKAINA, HUSSAIN])
    g3 = grouper.Group([ZAIN])
    g.add_group(g1)
    g.add_group(g2)
    g.add_group(g3)
    s = create_survey()
    f = s.score_grouping(g)
    assert f == 1.9905660377358492


def test_score_grouping_heterogenous() -> None:
    """Test score_grouping for a survey with 4 questions and a grouping
    with 3 groups (total 5 students). The criteria is all set to Heterogenous"""
    g = grouper.Grouping()
    g1 = grouper.Group([AREEJ, ALYZEH])
    g2 = grouper.Group([SUKAINA, HUSSAIN])
    g3 = grouper.Group([ZAIN])
    g._default_criterion = criterion.HeterogeneousCriterion()
    g.add_group(g1)
    g.add_group(g2)
    g.add_group(g3)
    s = create_survey()
    f = s.score_grouping(g)
    assert f == 1.9905660377358492


def test_student_has_answer() -> None:
    """Test student has answer method"""
    s = course.Student(10, "Fizzah")
    q = survey.Question(1, "What is your name?")
    ans = survey.Answer("Fizzah")
    s.set_answer(q, ans)
    assert s.has_answer(q) is True


def test_student_get_answer() -> None:
    """Test student get answer method"""
    s = course.Student(10, "Fizzah")
    q = survey.Question(1, "What is your name?")
    ans = survey.Answer("Fizzah")
    s.set_answer(q, ans)
    assert s.get_answer(q) == "Fizzah"


def test_course_all_answered() -> None:
    """Test course method enroll students"""
    students = create_students()
    history = course.Course('History101')
    history.enroll_students(students)
    survey1 = create_survey()
    assert history.all_answered(survey1) is True


def test_course_get_students() -> None:
    """Test course method get students"""
    students = create_students()
    history = course.Course('History101')
    history.enroll_students(students)
    assert history.get_students() == students


def test_homogenous_criterion_one(self=None) -> None:
    hom = criterion.HomogeneousCriterion
    q = survey.Question(1, "How old are you?")

    a1 = survey.Answer(10)
    assert hom.score_answers(self, q, [a1]) == 1.0


def test_heterogenous_criterion_two(self=None) -> None:
    het = criterion.HeterogeneousCriterion
    q = survey.Question(1, "How old are you?")
    a1 = survey.Answer(10)
    a2 = survey.Answer(12)
    assert het.score_answers(self, q, [a1,a2]) == 0.0


def test_homogenous_criterion_two(self=None) -> None:
    hom = criterion.HomogeneousCriterion
    q = survey.NumericQuestionQuestion(1, "How old are you?", 5, 16)
    a1 = survey.Answer(10)
    a2 = survey.Answer(12)
    assert hom.score_answers(self, q, [a1, a2]) == 1.0


def test_heterogenous_criterion_one(self=None) -> None:
    het = criterion.HeterogeneousCriterion
    q = survey.Question(1, "How old are you?")
    a1 = survey.Answer(10)
    a2 = survey.Answer(12)
    assert het.score_answers(self, q, [a1, a2]) == 0.0


def test_lonely_member_criterion(self=None) -> None:
    lonely = criterion.LonelyMemberCriterion
    q = survey.Question("How old are you?")
    a1 = survey.Answer(10)
    a2 = survey.Answer(12)
    assert lonely.score_answers(self, q, [a1, a2]) == 0.0


def test_lonely_member_criterion() -> None:
    lonely = criterion.LonelyMemberCriterion
    q = survey.Question(1, "How old are you?")
    a1 = survey.Answer(10)
    a2 = survey.Answer(12)
    a3 = survey.Answer(10)
    assert lonely.score_answers(q, [a1,a2,a3]) == 1.0


if __name__ == '__main__':
    import pytest
    pytest.main((['tests.py']))
