import pytest
from unittest.mock import MagicMock, patch
from src.models.token_nft import TokenNFT
from src.repositories.nft_repository import NFTRepository
from datetime import datetime
import uuid

@pytest.fixture
def sample_token():
    return TokenNFT(
        token_id=uuid.uuid4(),
        owner="user1",
        poll_id=uuid.uuid4(),
        option="Option A",
        issued_at=datetime.now()
    )

@patch("src.repositories.nft_repository.db.reference")
@patch("src.repositories.nft_repository.MongoClient")
def test_save_and_get(mock_mongo_client, mock_firebase_ref, sample_token):
    # Mock Firebase
    mock_ref_instance = MagicMock()
    mock_firebase_ref.return_value = mock_ref_instance
    
    # Mock Mongo
    mock_mongo_db = MagicMock()
    mock_mongo_collection = MagicMock()
    mock_mongo_client.return_value.__getitem__.return_value = mock_mongo_db
    mock_mongo_db.__getitem__.return_value = mock_mongo_collection
    
    repo = NFTRepository(mongo_uri="mongodb://localhost:27017")

    # Test save
    repo.save(sample_token)
    mock_ref_instance.child.assert_called_once_with(str(sample_token.token_id))
    mock_ref_instance.child().set.assert_called_once()
    mock_mongo_collection.update_one.assert_called_once()

    # Mock get in Firebase returns token dict
    mock_ref_instance.child().get.return_value = sample_token.to_dict()
    token = repo.get_by_id(str(sample_token.token_id))
    assert token.owner == "user1"

@patch("src.repositories.nft_repository.db.reference")
@patch("src.repositories.nft_repository.MongoClient")
def test_transfer_token(mock_mongo_client, mock_firebase_ref, sample_token):
    mock_ref_instance = MagicMock()
    mock_firebase_ref.return_value = mock_ref_instance
    mock_mongo_db = MagicMock()
    mock_mongo_collection = MagicMock()
    mock_mongo_client.return_value.__getitem__.return_value = mock_mongo_db
    mock_mongo_db.__getitem__.return_value = mock_mongo_collection

    repo = NFTRepository(mongo_uri="mongodb://localhost:27017")
    
    # Simula get_by_id con token
    repo.get_by_id = MagicMock(return_value=sample_token)
    repo.save = MagicMock()

    success = repo.transfer(str(sample_token.token_id), "user2")
    assert success
    assert sample_token.owner == "user2"
    repo.save.assert_called_once_with(sample_token)

    # Transferencia token no existente
    repo.get_by_id = MagicMock(return_value=None)
    success = repo.transfer("fake-id", "user2")
    assert not success