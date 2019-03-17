"""
This file is part of nucypher.

nucypher is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

nucypher is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with nucypher.  If not, see <https://www.gnu.org/licenses/>.
"""

import maya

from nucypher.blockchain.eth.constants import (MIN_ALLOWED_LOCKED,
                                               MAX_ALLOWED_LOCKED,
                                               MIN_LOCKED_PERIODS,
                                               MAX_MINTING_PERIODS,
                                               SECONDS_PER_PERIOD)


def datetime_to_period(datetime: maya.MayaDT) -> int:
    """Converts a MayaDT instance to a period number."""
    future_period = datetime.epoch // int(SECONDS_PER_PERIOD)
    return int(future_period)


def datetime_at_period(period: int) -> maya.MayaDT:
    """Returns the datetime object at a given period, future, or past."""

    now = maya.now()
    current_period = datetime_to_period(datetime=now)
    delta_periods = period - current_period

    # +
    if delta_periods:
        target_period = now + maya.timedelta(days=delta_periods)

    # -
    else:
        target_period = now - maya.timedelta(days=delta_periods)

    return target_period


def calculate_period_duration(future_time: maya.MayaDT) -> int:
    """Takes a future MayaDT instance and calculates the duration from now, returning in periods"""
    future_period = datetime_to_period(datetime=future_time)
    current_period = datetime_to_period(datetime=maya.now())
    periods = future_period - current_period
    return periods


def __validate(rulebook) -> bool:
    """Validate a rulebook"""
    for rule, failure_message in rulebook:
        if not rule:
            raise ValueError(failure_message)
    return True


def validate_stake_amount(amount, raise_on_fail=True) -> bool:
    """Validate a single staking value against pre-defined requirements"""
    from nucypher.blockchain.eth.currency import NU

    min_locked = NU(MIN_ALLOWED_LOCKED, 'NUWei')
    max_locked = NU(MAX_ALLOWED_LOCKED, 'NUWei')

    rulebook = (

        (min_locked <= amount,
         'Stake amount too low; ({amount}) must be at least {minimum}'
         .format(minimum=min_locked, amount=amount)),

        (max_locked >= amount,
         'Stake amount too high; ({amount}) must be no more than {maximum}.'
         .format(maximum=max_locked, amount=amount)),
    )

    if raise_on_fail is True:
        __validate(rulebook=rulebook)
    return all(rulebook)


def validate_locktime(lock_periods: int, raise_on_fail=True) -> bool:
    """Validate a single staking lock-time against pre-defined requirements"""

    rulebook = (

        (MIN_LOCKED_PERIODS <= lock_periods,
         'Locktime ({locktime}) too short; must be at least {minimum}'
         .format(minimum=MIN_LOCKED_PERIODS, locktime=lock_periods)),

        (MAX_MINTING_PERIODS >= lock_periods,
         'Locktime ({locktime}) too long; must be no more than {maximum}'
         .format(maximum=MAX_MINTING_PERIODS, locktime=lock_periods)),
    )

    if raise_on_fail is True:
        __validate(rulebook=rulebook)
    return all(rulebook)
