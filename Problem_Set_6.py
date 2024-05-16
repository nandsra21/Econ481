# Exercise 0

def github() -> str:
    """
    my github repo
    """

    return "https://github.com/nandsra21/Econ481/blob/main/Problem_Set_6.py"

# Exercise 1

def std() -> str:
    """
    Some docstrings.
    """
    query = '''
    SELECT itemId, 
           SQRT(SUM((bidAmount - avg_bidAmount) * (bidAmount - avg_bidAmount)) / (COUNT(bidAmount) - 1)) AS std
    FROM (
        SELECT itemId, bidAmount, AVG(bidAmount) OVER (PARTITION BY itemId) AS avg_bidAmount
        FROM bids
    ) AS subquery
    GROUP BY itemId
    HAVING COUNT(bidAmount) > 1
    '''

    return query

# Exercise 2

def bidder_spend_frac() -> str:
    """
    Docstring
    """
    query = '''
    WITH MaxBids AS (
        SELECT 
            bidderName, 
            itemId, 
            MAX(bidAmount) AS max_bid
        FROM 
            bids
        GROUP BY 
            itemId
    ),
    TotalSpend AS (
        SELECT 
            bidderName, 
            SUM(max_bid) AS total_spend
        FROM 
            MaxBids
        GROUP BY 
            bidderName
    ),
    BidAmount AS (
        SELECT 
            bidderName, 
            MAX(bidAmount) AS bids_amt
        FROM 
            bids
        GROUP BY 
            bidderName, itemId 
    ),
    TotalBids AS (
        SELECT
            bidderName,
            SUM(bids_amt) AS total_bids
        FROM
            BidAmount
        GROUP BY
            bidderName
    )       
    SELECT 
        ts.bidderName,
        ts.total_spend,
        tb.total_bids,
        CASE
            WHEN tb.total_bids > 0 
            THEN ts.total_spend * 1.0 / tb.total_bids
            ELSE 0
        END AS spend_frac
    FROM 
        TotalSpend ts
    JOIN 
        TotalBids tb ON ts.bidderName = tb.bidderName;
    '''
    return query

# Exercise 3

def min_increment_freq() -> str:
    """
    Docstring
    """
    query = """
    SELECT 
        COUNT(*) * 1.0 / (SELECT COUNT(*) FROM bids WHERE itemId IN (SELECT itemId FROM items WHERE isBuyNowUsed = 0)) AS freq
    FROM 
        bids b1
    JOIN 
        items i ON b1.itemId = i.itemId
    WHERE 
        i.isBuyNowUsed = 0
        AND b1.bidAmount = (
            SELECT MAX(b2.bidAmount)
            FROM bids b2
            WHERE b2.itemId = b1.itemId 
                AND b2.bidTime < b1.bidTime
        ) + i.bidIncrement;
    """
    return query

# Exercise 4

def win_perc_by_timestamp() -> str:
    """
    Docstring
    """

    query = """
    WITH AuctionTimes AS (
        SELECT
            itemId,
            MIN(bidTime) AS auctionStartTime,
            MAX(bidTime) AS auctionEndTime
        FROM 
            bids
        GROUP BY 
            itemId
    ),
    BinnedBids AS (
        SELECT
            b.itemId,
            b.bidderName,
            b.bidAmount,
            ((julianday(b.bidTime) - julianday(a.auctionStartTime)) / 
            (julianday(a.auctionEndTime) - julianday(a.auctionStartTime))) AS normalized_time,
            CASE
                WHEN ((julianday(b.bidTime) - julianday(a.auctionStartTime)) / 
                     (julianday(a.auctionEndTime) - julianday(a.auctionStartTime))) <= 0.1 THEN 1
                WHEN ((julianday(b.bidTime) - julianday(a.auctionStartTime)) / 
                     (julianday(a.auctionEndTime) - julianday(a.auctionStartTime))) <= 0.2 THEN 2
                WHEN ((julianday(b.bidTime) - julianday(a.auctionStartTime)) / 
                     (julianday(a.auctionEndTime) - julianday(a.auctionStartTime))) <= 0.3 THEN 3
                WHEN ((julianday(b.bidTime) - julianday(a.auctionStartTime)) / 
                     (julianday(a.auctionEndTime) - julianday(a.auctionStartTime))) <= 0.4 THEN 4
                WHEN ((julianday(b.bidTime) - julianday(a.auctionStartTime)) / 
                     (julianday(a.auctionEndTime) - julianday(a.auctionStartTime))) <= 0.5 THEN 5
                WHEN ((julianday(b.bidTime) - julianday(a.auctionStartTime)) / 
                     (julianday(a.auctionEndTime) - julianday(a.auctionStartTime))) <= 0.6 THEN 6
                WHEN ((julianday(b.bidTime) - julianday(a.auctionStartTime)) / 
                     (julianday(a.auctionEndTime) - julianday(a.auctionStartTime))) <= 0.7 THEN 7
                WHEN ((julianday(b.bidTime) - julianday(a.auctionStartTime)) / 
                     (julianday(a.auctionEndTime) - julianday(a.auctionStartTime))) <= 0.8 THEN 8
                WHEN ((julianday(b.bidTime) - julianday(a.auctionStartTime)) / 
                     (julianday(a.auctionEndTime) - julianday(a.auctionStartTime))) <= 0.9 THEN 9
                ELSE 10
            END AS timestamp_bin
        FROM
            bids b
        JOIN
            AuctionTimes a ON b.itemId = a.itemId
    ),
    MaxBids AS (
        SELECT 
            bidderName, 
            itemId, 
            MAX(bidAmount) AS max_bid
        FROM 
            bids
        GROUP BY 
            itemId
    ),
    BinnedWinningBids AS (
        SELECT
            b.itemId,
            b.bidderName,
            b.timestamp_bin
        FROM
            BinnedBids b
        JOIN
            MaxBids w ON b.itemId = w.itemId AND b.bidAmount = w.max_bid
    )
    SELECT
        timestamp_bin,
        COUNT(b.itemId) * 1.0 / (SELECT COUNT(*) FROM BinnedBids WHERE BinnedBids.timestamp_bin = b.timestamp_bin) AS win_perc
    FROM
        BinnedWinningBids b
    GROUP BY
        timestamp_bin;
    """
    return query