import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

#1
def test_add_multiple_choices_increments_count_and_sequential_ids():
    question = Question(title='q1')
    choice1 = question.add_choice('Choice 1', False)
    choice2 = question.add_choice('Choice 2', False)
    assert len(question.choices) == 2
    assert choice2.id == choice1.id + 1

#2
def test_choice_empty_text_raises_exception():
    question = Question(title='q1')
    with pytest.raises(Exception) as exc_info:
        question.add_choice('', False)
    assert 'Text cannot be empty' in str(exc_info.value)

#3
def test_choice_text_length_exceeds_limit_raises_exception():
    question = Question(title='q1')
    long_text = 'a' * 101
    with pytest.raises(Exception) as exc_info:
        question.add_choice(long_text, False)
    assert 'Text cannot be longer than 100 characters' in str(exc_info.value)

#4
def test_remove_choice_by_id_removes_the_choice():
    question = Question(title='q1')
    choice = question.add_choice('Choice to remove', False)
    initial_count = len(question.choices)
    question.remove_choice_by_id(choice.id)
    assert len(question.choices) == initial_count - 1
    with pytest.raises(Exception):
        question.remove_choice_by_id(choice.id)

#5
def test_remove_choice_by_invalid_id_raises_exception():
    question = Question(title='q1')
    question.add_choice('Choice 1', False)
    # Tentar remover um ID inexistente deve lançar exceção
    with pytest.raises(Exception) as exc_info:
        question.remove_choice_by_id(999)
    assert 'Invalid choice id' in str(exc_info.value)

#6
def test_remove_all_choices_clears_all_choices():
    question = Question(title='q1')
    question.add_choice('Choice 1', False)
    question.add_choice('Choice 2', True)
    question.remove_all_choices()
    assert len(question.choices) == 0

#7
def test_select_choices_returns_correct_ids_when_correct_choice_selected():
    question = Question(title='q1', max_selections=2)
    c1 = question.add_choice('Choice 1', False)
    c2 = question.add_choice('Choice 2', False)
    c3 = question.add_choice('Choice 3', False)
    question.set_correct_choices([c2.id, c3.id])
    selected_ids = [c2.id, c3.id]
    result = question.select_choices(selected_ids)
    assert set(result) == set(selected_ids)

#8
def test_select_choices_returns_empty_when_wrong_choice_selected():
    question = Question(title='q1', max_selections=2)
    c1 = question.add_choice('Choice 1', False)
    c2 = question.add_choice('Choice 2', False)
    question.set_correct_choices([c2.id])
    result = question.select_choices([c1.id])
    assert result == []

#9
def test_select_choices_exceeds_max_selections_raises_exception():
    question = Question(title='q1', max_selections=1)
    c1 = question.add_choice('Choice 1', False)
    c2 = question.add_choice('Choice 2', True)
    with pytest.raises(Exception) as exc_info:
        question.select_choices([c1.id, c2.id])
    assert 'Cannot select more than' in str(exc_info.value)

#10
def test_set_correct_choices_updates_choice_correctness():
    question = Question(title='q1')
    c1 = question.add_choice('Choice 1', False)
    c2 = question.add_choice('Choice 2', False)
    assert not c1.is_correct
    assert not c2.is_correct
    question.set_correct_choices([c2.id])
    assert not c1.is_correct
    assert c2.is_correct