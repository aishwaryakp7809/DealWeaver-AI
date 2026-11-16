
import pytest

from agents.mediator_agent import check_feasibility


def test_feasible_price_range():
    result = check_feasibility(4000, 3500)

    assert result["feasible"] is True
    assert result["no_feasible_deal"] is False
    assert result["midpoint"] == 3750


def test_no_feasible_price_range():
    result = check_feasibility(3000, 3500)

    assert result["feasible"] is False
    assert result["no_feasible_deal"] is True
    assert result["midpoint"] is None


def test_equal_buyer_max_and_seller_min():
    result = check_feasibility(3500, 3500)

    assert result["feasible"] is True
    assert result["midpoint"] == 3500


def test_proposed_price_within_limits():
    result = check_feasibility(4000, 3500, 3750)

    assert result["proposed_price_feasible"] is True


def test_proposed_price_outside_limits():
    result = check_feasibility(4000, 3500, 4200)

    assert result["feasible"] is True
    assert result["proposed_price_feasible"] is False


@pytest.mark.parametrize(
    "buyer_max, seller_min",
    [
        (0, 3500),
        (-100, 3500),
        (4000, 0),
        (4000, -100),
        (float("inf"), 3500),
        (4000, float("nan")),
        (True, 3500),
        ("4000", 3500),
    ]
)
def test_invalid_prices_are_rejected(buyer_max, seller_min):
    with pytest.raises(ValueError):
        check_feasibility(buyer_max, seller_min)
