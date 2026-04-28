from lint.uuid_quality import check_uuid


def test_valid_v4_passes():
    assert check_uuid("2cfdf745-85a0-41be-9d93-1f89e5b70de7") is None


def test_valid_v5_passes():
    assert check_uuid("037da6b1-3c6d-5522-99c8-b916b4a26f00") is None


def test_valid_v7_passes():
    assert check_uuid("019adb84-22bb-7187-bf34-982378e7e0b9") is None


def test_sentinel_zero_uuid_passes():
    assert check_uuid("00000000-0000-0000-0000-000000000000") is None


def test_non_v4_rejected():
    # v1 UUID
    assert check_uuid("123e4567-e89b-12d3-a456-426614174000") is not None


def test_no_version_rejected():
    assert check_uuid("1a6f8b4d-3e9c-4a5f-2d7b-6c8e9f3b7d2a") is not None


def test_interleaved_sequence_e1d2c3b4():
    # Valid v4 format but clearly hand-typed
    assert check_uuid("e1d2c3b4-a5f6-4e7d-8c9b-0a1b2c3d4e5f") is not None


def test_interleaved_sequence_a7b8c9d0():
    assert check_uuid("a7b8c9d0-e1f2-4a3b-5c6d-7e8f9a0b1c2d") is not None


def test_straight_sequence_12345678():
    assert check_uuid("12345678-1234-1234-1234-123456789123") is not None


def test_interleaved_sequence_a1b2c3d4():
    assert check_uuid("a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d") is not None


def test_real_world_uuid_not_flagged():
    # Randomly generated UUIDs from the nlu-runtime codebase
    assert check_uuid("66bdefbe-74fa-4a25-bbaf-d44260927af4") is None
    assert check_uuid("901f1282-73d7-4952-b048-00ab694d6744") is None
    assert check_uuid("fd99e55b-3b2c-43e8-a2c0-6d5e5adea31f") is None


def test_scheduling_eligibility_bb_flagged():
    # Known bad UUID already in the codebase
    assert check_uuid("a3c7f8d2-9b4e-4a1c-8f2d-5e6a7b8c9d0e") is not None


def test_invalid_uuid_string():
    assert check_uuid("not-a-uuid-at-all-nope-nope12345678") is not None
